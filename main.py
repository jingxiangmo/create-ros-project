import questionary
from utils import *
from ros_installer import *


def ros_compatibility(ros_version, architecture_type, os_type):
    ros1_compatibility_map = {
        ('amd64', 'Ubuntu 20.04'): ['ROS 1 Noetic Ninjemys'],
        ('arm64', 'Ubuntu 20.04'): ['ROS 1 Noetic Ninjemys'],
        ('amd64', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
        ('armhf', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
        ('arm64', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
        ('amd64', 'Ubuntu 17.10'): ['ROS 1 Melodic'],

    }

    ros2_compatibility_map = {
        ('amd64', 'Ubuntu 20.04'): ['ROS 2 Foxy'],
        ('arm64', 'Ubuntu 20.04'): ['ROS 2 Foxy'],
        ('arm32', 'Ubuntu 20.04'): ['ROS 2 Foxy '],
        ('amd64', 'Ubuntu 22.04'): ['ROS 2 Iron'],
        ('arm64', 'Ubuntu 22.04'): ['ROS 2 Iron'],
        ('amd64', 'macOS'): ['ROS 2 Iron'],
        ('amd64', 'macOS 10.14'): ['ROS 2 Foxy'],
    }

    if ros_version == "ROS 1":
        return ros1_compatibility_map.get((architecture_type, os_type), [])
    if ros_version == "ROS 2":
        return ros2_compatibility_map.get((architecture_type, os_type), [])


def install_ros(architecture_type, os_type):
    version = questionary.select(
        "Which version of ROS would you like to install?",
        choices=['ROS 1', 'ROS 2'],
    ).ask()

    print(f"\nYour computer uses {architecture_type} architecture and {os_type} OS.\n")

    if version == 'ROS 1':

        distribution = questionary.select(
            "Which available ROS 1 distribution (based on your computer architecture and OS) would you like to install?",
            choices=['ROS 1 Noetic', 'ROS 1 Melodic'],
        ).ask()
    else:
        distribution = questionary.select(
            "Which available ROS 2 distribution (based on your computer architecture and OS) would you like to install?",
            choices=['ROS 2 Iron', 'ROS 2 Foxy'],
        ).ask()

    return version, distribution


if __name__ == "__main__":

    print("""        ;     /        ,--.     
       ["]   ["]  ,<  |__**|    
      /[_]\  [~]\/    |//  |    
       ] [   OOO      /o|__|   ROS
    """)

    project_name = questionary.text("What is your project named?",
                                    validate=lambda text: True if len(text) > 0 else "Please give your project a name!"
                                    ).ask()

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
            ros_version, ros_distribution = install_ros(architecture_type, os_type)

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

    confirm_install = questionary.confirm(
        "Ok to proceed? The project will be setup and created.", default=True
    ).ask()

    if confirm_install:
        run_ros_install(ros_version, ros_distribution)
        create_project_files(project_name, license_type, ros_distro, git_init)
    else:
        print("You've quit installation :(")
