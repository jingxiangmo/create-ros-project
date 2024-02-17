import questionary
import yaml
from utils import *
from ros_installer import *

def install_ros(architecture_type, os_name, os_version):
    version = questionary.select(
        "Which version of ROS would you like to install?",
        choices=['ROS 1', 'ROS 2'],
    ).ask()

    file_path = 'ros_compatibility.yaml'
    with open(file_path, 'r') as file:
        compatibility = yaml.safe_load(file)

    distribution = questionary.select(
        "Which available ROS distribution would you like to install? This is based on your current os and cpu architecture.",
        choices=compatibility[version][architecture_type][os_name][os_version]
    ).ask()

    return version, distribution

def script():
    print("""        ;     /        ,--.     
       ["]   ["]  ,<  |__**|    
      /[_]\  [~]\/    |//  |    
       ] [   OOO      /o|__|   ROS
    """)

    project_name = questionary.text("What is your project named?",
                                    validate=lambda text: True if len(text) > 0 else "Please give your project a name!"
                                    ).ask()

    architecture_type, os_name, os_version = get_system_info()
    ros_installed, ros_distro = check_ros_installation()

    print(f"\nYour computer uses {architecture_type} architecture and {os_name} {os_version} OS. {f'Current ROS version: {ros_distro}' if ros_installed else 'ROS is not installed.'}\n")


    if not ros_installed:
        # try:
        install_ros(architecture_type, os_name, os_version)
        # except KeyError:
        #     print("There are currently no available ROS distribution available your computer architecture and OS.")
    else:
        new_ros = questionary.confirm(
            "What you like to install another ROS version instead?", default=False
        ).ask()
        if new_ros:
            ros_version, ros_distribution = install_ros(architecture_type, os_name, os_version)

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

if __name__ == "__main__":
    script()