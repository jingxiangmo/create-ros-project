import questionary
from utils import *
from ros_installer import *

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
    ros_installed, ros_version, ros_distribution = check_ros_installation()
    to_install_ros = False

    print(f"\nYour computer uses {architecture_type} architecture and {os_name} {os_version} OS. {f'{ros_version} installed with {ros_distribution} distribution' if ros_installed else 'ROS is not installed.'}\n")

    if not ros_installed:
        try:
            ros_version, ros_distribution = install_ros_prompt(architecture_type, os_name, os_version)
            to_install_ros = True
        except KeyError:
            print("There are currently no available ROS distribution available your computer architecture and OS.")
    else:
        new_ros = questionary.confirm(
            "What you like to install another ROS version instead?", default=False
        ).ask()
        if new_ros:
            ros_version, ros_distribution = install_ros_prompt(architecture_type, os_name, os_version)
            to_install_ros = True

    license_type = questionary.select(
        "Which license would you like to choose?",
        choices=['MIT', 'Apache-2.0', 'BSD'],
    ).ask()

    project_language = questionary.select(
        "Would like to use ROS C++ or ROS Python?",
        choices=['C++ and Python (recommended)', 'C++ only', 'Python only']
    ).ask()

    project_template = questionary.select(
        "Would like to start with a project template?",
        choices=['Basic Workspace (recommended)', 'Empty Workspace']
    )

    git_init = questionary.confirm(
        "Initialize a new git repository? (optional)", default=True
    ).ask()

    confirm_install = questionary.confirm(
        "Ok to proceed? The project will be setup and created.", default=True
    ).ask()

    if confirm_install:
        if to_install_ros:
            run_ros_install(ros_version, ros_distribution)

        create_project_files(project_name, license_type, ros_version, ros_distribution, git_init)
    else:
        print("You've quit installation :(")

if __name__ == "__main__":
    script()