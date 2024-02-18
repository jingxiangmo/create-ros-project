import subprocess
import platform
import toml
import os
from typing import Tuple
import questionary
import yaml

def run_command(command : str):
    try:
        result = subprocess.run(
            command,
            shell=False,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None

def get_system_info() -> Tuple[str, str, str]:
    try:
        basic_platform = platform.platform(aliased=True, terse=True)
        if platform.system() == 'Darwin':
            os_name = "MacOS"
            os_version = platform.mac_ver()[0]
        elif platform.system() == 'Linux':
            os_name, os_version = basic_platform.split('-')[0], basic_platform.split('-')[1]
        else:
            os_name_version = basic_platform.split('-')[0]
            os_name, os_version = os_name_version.rsplit(' ', 1)

        return platform.machine(), os_name, str(os_version)

    except:
        print("Could not get system info.")

def install_ros_prompt(architecture_type: str, os_name: str, os_version: str) -> Tuple[str, str]:
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

def check_ros_installation() -> Tuple[bool, str, str]:
    try:
        ros_version = os.getenv('ROS_VERSION')
        ros_distribution = subprocess.check_output(['rosversion', '-d'], universal_newlines=True).strip()
        return True, "ROS " + ros_version, ros_distribution
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None, None

def create_project_files(project_name : str, license_type : str, ros_version : str, ros_distribution : str, git_init : bool):

    os.makedirs(project_name, exist_ok=True)

    toml_file_path = os.path.join(project_name, 'rosproject.toml')
    readme_file_path = os.path.join(project_name, 'README.md')
    src_directory_path = os.path.join(project_name, 'src')
    git_ignore_path = os.path.join(project_name, '.gitignore')

    data = {
        "project": {
            "name": project_name,
            "license": license_type,
            "readme": "README.md"
        },
        "dependencies": {
            "ros": ros_distribution,
        },
        "packages": {},
    }

    with open(toml_file_path, 'w') as file:
        toml.dump(data, file)

    with open(readme_file_path, 'w') as file:
        file.write(f"# {project_name}\n")

    os.makedirs(src_directory_path, exist_ok=True)

    if git_init:
        run_command("git init")
        with open(git_ignore_path, 'w') as file:
            file.write(".idea")

    print(f"\n{project_name} setup is complete. Welcome to ROS.\n")
