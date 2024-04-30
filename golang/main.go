/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>

*/
package main

import (
    "bytes"
    "fmt"
    "io"
    "log"
    "net/http"
    "os"
    "os/exec"
    "path/filepath"
    "runtime"

    "github.com/charmbracelet/huh"
    "github.com/pelletier/go-toml/v2" // already used by viper
    "github.com/shirou/gopsutil/v3/host"
)

func main() {

    fmt.Println(
`  ;     /        ,--.
  ["]   ["]  ,<  |__**|
 /[_]\  [~]\/    |//  |
  ] [   OOO      /o|__|   ROS`)
    var (
        OSdistro           string
        OSversion          string

        rosVersion         string
        rosDistro          string

        projectName        string

        // REVIEW: these are viable candidates for a config file or flags
        license            string
        cppAndOrPython     string
        template           string
        shouldInitGit      bool
        shouldInstallROS   bool

        confirm            bool
    )

    {
        // TODO: handle error
        hostinfo, _ := host.Info()
        OSdistro, OSversion = hostinfo.Platform, hostinfo.PlatformVersion
        fmt.Printf(
            "OS: %s\nDistro: %s\nVersion: %s\nArch: %s\n",
            runtime.GOOS,
            OSdistro,
            OSversion,
            runtime.GOARCH,
        )
    }


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
        log.Fatal(err)
    }


    // - https://github.com/ros-infrastructure/rospkg/blob/c8185799792c86b1c9a8df2c1a24da85c2b49b9f/src/rospkg/rosversion.py#L118-L122
    // - https://github.com/ros-infrastructure/rospkg/blob/c8185799792c86b1c9a8df2c1a24da85c2b49b9f/src/rospkg/rosversion.py#L39-L45
    // NOTE(beau): from
    // very old ROS distributions don't set the ROS_DISTRO environment
    // variable rosversion provides a way to find this that we can copy. We
    // can't call rosversion directly because the expectation is zero
    // dependencies. Perhaps we could optionally use it if it's available.
    // TODO: find older ROS versions using the logic from rosversion linked
    // above
    rosVersion, rosDistro = os.Getenv("ROS_VERSION"), os.Getenv("ROS_DISTRO")
    {
        rosInstalled := len(rosVersion) > 0 && len(rosDistro) > 0
        if rosInstalled {
            title := fmt.Sprintf("Looks like you have ROS %s %s installed, would you like to install another ROS version instead?", rosVersion, rosDistro)
            if err := huh.NewConfirm().
                Title(title).
                Value(&shouldInstallROS).
                Run();
            err != nil {
                log.Fatal(err)
            }
        } else {
            shouldInstallROS = true
        }
    }

    if shouldInstallROS {
        rosCompatibility := map[string]map[string]map[string]map[string][]string {
            "ROS 1": {
                "amd64": {
                    "ubuntu": {
                        "20.04": { "Noetic"  },
                        "18.04": { "Melodic" },
                    },
                },
                "arm64": {
                    "ubuntu": {
                        "20.04": { "Noetic"  },
                        "18.04": { "Melodic" },
                    },
                },
            },
            "ROS 2": {
                "amd64": {
                    "ubuntu": {
                        "20.04": { "Iron" },
                        "18.04": { "Foxy" },
                    },
                },
                "arm64": {
                    "darwin": {
                        "14.4.1": {
                            "Test 1",
                            "Test 2",
                        },
                    },
                    "ubuntu": {
                        "20.04": { "Iron" },
                        "18.04": { "Foxy" },
                    },
                },
            },
        }

        // TODO: find this out regardless of if we're installing
        if err := huh.NewSelect[string]().
            Title("Which version of ROS would you like to install?").
            Options(huh.NewOptions("ROS 2", "ROS 1")...).
            Value(&rosVersion).
            Run();
        err != nil {
            log.Fatal(err)
        }

        options, exists := rosCompatibility [rosVersion][runtime.GOARCH][OSdistro][OSversion]

        if exists {
            if err := huh.NewSelect[string]().
                Title("Which available ROS distribution would you like to install? This is based on your current os and cpu architecture.").
                Options(huh.NewOptions(options...)...).
                Value(&rosDistro).
                Run();
             err != nil {
                log.Fatal(err)
            }
        } else {
            log.Fatal("No compatible ROS distributions available")
        }

    }

    form := huh.NewForm(
        huh.NewGroup(
            huh.NewSelect[string]().
                Title("What license do you want to use?").
                Options(huh.NewOptions("MIT", "Apache-2.0", "BSD")...).
                Value(&license),
            ),

        huh.NewGroup(
            huh.NewSelect[string]().
                Title("Would like to use ROS C++ or ROS Python?").
                Options(huh.NewOptions("C++ and Python (recommended)", "C++ only", "Python only")...).
                Value(&cppAndOrPython),
            ),

        huh.NewGroup(
            huh.NewSelect[string]().
                Title("Would like to start with a project template?").
                Options(huh.NewOptions("Basic Workspace (recommended)", "Empty Workspace")...).
                Value(&template),
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
        log.Fatal(err)
    }


    if !confirm {
        log.Fatal("user aborted")
    }

    srcPath := filepath.Join(projectName, "src")

    // makes the project folder as well since its a parent of src
    // REVIEW(beau): permissions
    if err := os.MkdirAll(srcPath, 0755);
    err != nil {
        log.Fatal(err)
    }

    // NOTE(beau): should be safe because we just created the directory
    os.Chdir(projectName)

    if shouldInitGit {
        // TODO: handle error
        exec.Command("git", "init").Run()

        // get a good gitignore template
        ignoreAPI_URL := "https://www.toptal.com/developers/gitignore/api/ros"
        if rosVersion == "ROS 2" {
            ignoreAPI_URL += "2"
        }

        // TODO: handle errors
        resp, _ := http.Get(ignoreAPI_URL)
        body, _ := io.ReadAll(resp.Body)

        // REVIEW(beau): file permissions. smh
        os.WriteFile(".gitignore", body, 0644)
    }

    os.WriteFile("README.md", []byte(fmt.Sprintf("# %s\n\n", projectName)), 0644)

    tomlbuf := bytes.Buffer{}
    toml.NewEncoder(&tomlbuf).Encode(map[string]map[string]string {
        "project": {
            "name": projectName,
            "license": license,
            "readme": "README.md",
        },
        "dependencies": {
            "ros": rosDistro,
        },
        "packages": {},
    })

    os.WriteFile("rosproject.toml", tomlbuf.Bytes(), 0644)
}
