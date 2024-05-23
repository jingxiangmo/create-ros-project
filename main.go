package main

import (
    "bytes"
    "fmt"
    "io"
    "net/http"
    "os"
    "os/exec"
    "path/filepath"

    _ "embed"

    "github.com/charmbracelet/huh"
    "github.com/pelletier/go-toml/v2" // already used by viper
    "github.com/shirou/gopsutil/v3/host"

    "github.com/go-git/go-git/v5"

    docker "github.com/docker/docker/client"
)

type ROSDistro int
const (
    Jazzy ROSDistro = iota
    Humble
    Noetic
)

func (distro ROSDistro) String() string {
    return [...]string{"ROS 2 Jazzy", "ROS 2 Humble", "ROS 1 Noetic"}[distro]
}

func (distro ROSDistro) IsRos2() bool {
    if distro == Noetic {
        return false
    }

    return true
}

// NOTE(beau): do not mutate. Maps each supported distro to their $ROS_DISTRO
var rosDistroEnvVar = map[ROSDistro]string {
    Jazzy: "jazzy",
    Humble: "humble",
    Noetic: "noetic",
}

type License int
const (
    Apache2 License = iota
    MIT
    BSD3
    None
)

func (license License) String() string {
    return [...]string{"Apache-2.0", "MIT", "BSD-3-Clause", "None"}[license]
}

type ROSInstallType int
const (
    DockerInstall ROSInstallType = iota
    NativeInstall
    ExisitingNativeInstall
)

func (install ROSInstallType) String() string {
    return [...]string{"Docker Install (recommended)", "Native Install", "Existing Native Install"}[install]
}

// embedded files
var (
    //go:embed ros_install_scripts/ubuntuROS1.sh
    ubuntuROS1 string

    //go:embed ros_install_scripts/ubuntuROS1.sh
    ubuntuROS2 string


    //go:embed licenses/mit
    mitLicense []byte

    //go:embed licenses/apache2
    apache2License []byte

    //go:embed licenses/bsd3
    bsd3License []byte
)

func run() error {
    fmt.Println(
`  ;     /        ,--.
  ["]   ["]  ,<  |__**|
 /[_]\  [~]\/    |//  |
  ] [   OOO      /o|__|   ROS`)
    var (
        projectName        string

        possibleInstalls = []ROSInstallType{DockerInstall}
        installType        ROSInstallType

        installDistro      ROSDistro

        license            License
        shouldInitGit      bool

        confirm            bool
    )

    if err := huh.NewInput().
        Title("What is your project named?").
        Prompt("? ").
        // TODO: enforce a valid directory name
        Validate(func(projName string) (result error) {
            if len(projName) < 1 {
                result = fmt.Errorf("Project name cannot be empty")
            }
            return
        }).
        Value(&projectName).
        Run();
    err != nil {
        return err
    }

    hostinfo, err := host.Info()
    if err != nil {
        return err
    }

    info := ""
    // determine if native and existing installs are possible
    if hostinfo.Platform == "ubuntu" {
        possibleInstalls = append(possibleInstalls, NativeInstall)
        // - https://github.com/ros-infrastructure/rospkg/blob/c8185799792c86b1c9a8df2c1a24da85c2b49b9f/src/rospkg/rosversion.py#L118-L122
        // - https://github.com/ros-infrastructure/rospkg/blob/c8185799792c86b1c9a8df2c1a24da85c2b49b9f/src/rospkg/rosversion.py#L39-L45
        // NOTE(beau): from
        // very old ROS distributions don't set the ROS_DISTRO environment
        // variable rosversion provides a way to find this that we can copy. We
        // can't call rosversion directly because the expectation is zero
        // dependencies. Perhaps we could optionally use it if it's available.
        // TODO: find older ROS versions using the logic from rosversion linked
        // above

        installedDistro := os.Getenv("ROS_DISTRO")
        for distro, distroEnvVar := range rosDistroEnvVar {
            if installedDistro == distroEnvVar {
                possibleInstalls = append(possibleInstalls, ExisitingNativeInstall)
                info = fmt.Sprintf("Please select [%s] to use your existing installation of %s", ExisitingNativeInstall, distro)
                break
            }
        }

        if err := huh.NewSelect[ROSInstallType]().
            Title("How do you want to install ROS?" + info).
            Options(huh.NewOptions(possibleInstalls...)...).
            Value(&installType).
            Run();
        err != nil {
            return err
        }
    } else {
        installType = DockerInstall
    }

    switch installType {
    case DockerInstall:
        if err := huh.NewSelect[ROSDistro]().
            Title("What ROS distribution do you want to use?").
            Options(huh.NewOptions([]ROSDistro{Jazzy, Humble, Noetic}...)...).
            Value(&installDistro).
            Run();
        err != nil {
            return err
        }
        fmt.Println("Using Docker install of", installDistro)
    case NativeInstall:
        switch hostinfo.PlatformVersion {
        case "20.04": installDistro = Noetic
        case "22.04": installDistro = Humble
        case "24.04": installDistro = Jazzy
        default: return fmt.Errorf("Unsupported Ubuntu version %s", hostinfo.PlatformVersion)
        }
        fmt.Printf("Installing %s, as its compatible with your operating system\n", installDistro)
    case ExisitingNativeInstall: fmt.Println("Using existing installation")
    }

    form := huh.NewForm(
        huh.NewGroup(
            huh.NewSelect[License]().
                Title("What license do you want to use?").
                Options(huh.NewOptions(Apache2, MIT, BSD3, None)...).
                Value(&license),
            ),

        huh.NewGroup(
            huh.NewConfirm().
                Title("Initialize a new git repository? (optional)").
                Value(&shouldInitGit),
            ),

        huh.NewGroup(
            huh.NewConfirm().
                Title("Ok to proceed? The project will be setup and created.").
                Value(&confirm),
            ),
    )

    if err := form.Run();
    err != nil {
        return err
    }


    if !confirm {
        return fmt.Errorf("user aborted")
    }

    srcPath := filepath.Join(projectName, "src")

    // makes the project folder as well since its a parent of src
    // REVIEW(beau): permissions
    if err := os.MkdirAll(srcPath, 0755);
    err != nil {
        return err
    }

    // NOTE(beau): should be safe because we just created the directory
    os.Chdir(projectName)

    // REVIEW: its currently assumed that writing to files is safe because we
    // just created the directory

    if shouldInitGit {
        git.PlainInit(".", false)

        // get a good gitignore template
        ignoreAPI_URL := "https://www.toptal.com/developers/gitignore/api/ros"
        if installDistro.IsRos2() {
            ignoreAPI_URL += "2"
        }

        {
            resp, err := http.Get(ignoreAPI_URL)
            if err != nil {
                return err
            }
            // REVIEW(beau): is it safe to ignore this error since the request worked?
            body, _ := io.ReadAll(resp.Body)

            os.WriteFile(".gitignore", body, 0644)
        }
    }

    tomlbuf := bytes.Buffer{}
    if err := toml.NewEncoder(&tomlbuf).Encode(map[string]map[string]string {
        "project": {
            "name": projectName,
            "license": license.String(),
            "readme": "README.md",
        },
        "dependencies": {
            "ros": rosDistroEnvVar[installDistro],
        },
        "packages": {},
    }); err != nil {
        return err
    }

    os.WriteFile("rosproject.toml", tomlbuf.Bytes(), 0644)
    os.WriteFile("README.md", []byte(fmt.Sprintf("# %s\n\n", projectName)), 0644);

    {
        var choice []byte

        switch license {
        case Apache2: choice = apache2License
        case MIT:     choice = mitLicense
        case BSD3:    choice = bsd3License
        }
        os.WriteFile("LICENSE", choice, 0644)
    }

    switch installType {
    case DockerInstall:
    case NativeInstall:
        // INFO(beau): how we tell the install script what distro we're installing
        os.Setenv("CRP_ROSDISTRO", rosDistroEnvVar[installDistro])
        var execCmd string
        if installDistro.IsRos2() {
            execCmd = ubuntuROS2
        } else {
            execCmd = ubuntuROS1
        }
        exec.Command("sh", "-c", execCmd).Run()
    case ExisitingNativeInstall: // REVIEW(beau): is there anything to do here?
    }

    return nil
}

func main() {
    // TODO: something smarter
    if err := run(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
