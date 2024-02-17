import subprocess
import platform
import toml
import os
from ros_installer import *

def run_command(command, shell=False):
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None

def get_system_info():
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

def create_project_files(project_name, license_type, ros_distro, ros_version, ros_distribution, git_init):
    # setup project
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
            "ros": ros_distro,
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
