import questionary
import subprocess
import platform
import toml
import os


def run_command(command, shell=False):
    try:
        result = subprocess.run(command, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def get_os_description():
    basic_platform = platform.platform(aliased=True, terse=True)
    if platform.system() == 'Darwin':
        os_name = "MacOS"
        os_version = platform.mac_ver()[0]
    elif platform.system() == 'Linux':
        os_name, os_version = basic_platform.split('-')[0], basic_platform.split('-')[1]
    else:
        os_name_version = basic_platform.split('-')[0]
        os_name, os_version = os_name_version.rsplit(' ', 1)
    return f"{os_name} {os_version}"


def get_system_info():
    return platform.machine(), get_os_description()


def check_ros_installation():
    try:
        version_output = subprocess.check_output(['rosversion', '-d'], universal_newlines=True).strip()
        return True, version_output
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None

def install_ros(architecture_type, os_type):
    ros_version = questionary.select(
        "Which version of ROS would you like to install?",
        choices=['ROS 1', 'ROS 2'],
    ).ask()

    if (ros_version == 'ROS 1'):
        ros_distribution = questionary.select(
            "Which ROS 1 distribution would you like to install?",
            choices=['noetic', 'kinetic', 'melodic'],
        ).ask()
    else:
        ros_distribution = questionary.select(
            "Which ROS 2 distribution would you like to install?",
            choices=['galatic', 'foxy'],
        ).ask()

    confirm_install = questionary.confirm(
        "Ok to proceed?", default=True
    ).ask()

    return
    if confirm_install:
        run_ros_install()


def run_ros_install(ros_version, ros_distribution):
    if ros_version == "1":
        print("Installing ROS1...")
        # run(["sudo", "apt-get", "update"])
        # run(["sudo", "apt-get", "install", "-y", "ros-noetic-desktop-full"])
    elif ros_version == "2":
        print("Installing ROS2...")

        # see documentation: https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html

        # set locale
        run_command("locale")
        run_command("sudo apt update && sudo apt install locales")
        run_command("sudo locale-gen en_US en_US.UTF-8")
        run_command("sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8")
        run_command("export LANG=en_US.UTF-8")
        run_command("locale")

        # setup sources
        run_command("sudo apt install software-properties-common")
        run_command("sudo add-apt-repository universe")
        run_command("sudo apt update && sudo apt install curl -y")
        run_command(
            "sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg")
        run_command(
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null')

        # install ros2 packages
        run_command("sudo apt update")
        run_command("sudo apt upgrade")
        run_command("sudo apt install ros-" + ros_distribution + "python3-argcomplete")
        run_command("sudo apt install ros-dev-tools")

        # sourcing setup script

    print("ROS installation complete.")


def create_project_files(project_name, license_type, ros_distro):

    os.makedirs(project_name, exist_ok=True)

    toml_file_path = os.path.join(project_name, 'rosproject.toml')
    readme_file_path = os.path.join(project_name, 'README.md')
    src_directory_path = os.path.join(project_name, 'src')

    data = {
        "project": {
            "name": project_name,
            "license": license_type,
            "readme": "README.md"
        },
        "dependencies": {
            "ros": ros_distro,
        },
        "packages": {},
    }

    with open(toml_file_path, 'w') as file:
        toml.dump(data, file)

    with open(readme_file_path, 'w') as file:
        file.write(f"# {project_name}\n")

    os.makedirs(src_directory_path, exist_ok=True)


if __name__ == "__main__":

    print("""        ;     /        ,--.     
       ["]   ["]  ,<  |__**|    
      /[_]\  [~]\/    |//  |    
       ] [   OOO      /o|__|   ROS
""")

    project_name = questionary.text("What is your project named?",).ask()

    architecture_type, os_type = get_system_info()
    ros_installed, ros_distro = check_ros_installation()

    print(
        f"\nYour computer uses {architecture_type} architecture and {os_type} OS. {f'Current ROS version: {ros_distro}' if ros_installed else 'ROS is not installed.'}\n")

    if not ros_installed:
        install_ros(architecture_type, os_type)
    else:
        new_ros = questionary.confirm(
            "What you like to install another ROS version instead?", default=False
        ).ask()
        if new_ros:
            install_ros(architecture_type, os_type)

    license_type = questionary.select(
        "Which license would you like to choose?",
        choices=['MIT', 'Apache-2.0', 'BSD'],
    ).ask()

    project_language = questionary.select(
        "Would like to use ROS C++ or ROS Python?",
        choices=['C++ and Python (recommended)', 'C++ only', 'Python only']
    ).ask()

    git_init = questionary.confirm(
        "Initialize a new git repository? (optional)", default=True
    ).ask()

    create_project_files(project_name, license_type, ros_distro)

    print(f"{project_name} setup is complete.")
