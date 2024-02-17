import questionary
import os
from utils import *


def install_ros(architecture_type, os_type):
    ros_version = questionary.select(
        "Which version of ROS would you like to install?",
        choices=['ROS 1', 'ROS 2'],
    ).ask()

    if ros_version == 'ROS 1':
        ros_distribution = questionary.select(
            "Which ROS 1 distribution would you like to install?",
            choices=['noetic', 'kinetic', 'melodic'],
        ).ask()
    else:
        ros_distribution = questionary.select(
            "Which ROS 2 distribution would you like to install?",
            choices=['galatic', 'foxy'],
        ).ask()


if __name__ == "__main__":

    print("""        ;     /        ,--.     
       ["]   ["]  ,<  |__**|    
      /[_]\  [~]\/    |//  |    
       ] [   OOO      /o|__|   ROS
    """)

    project_name = questionary.text("What is your project named?", ).ask()

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
