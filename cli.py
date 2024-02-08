import questionary
import subprocess
import os

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def install_ros(version, distribution):
    if version == "1":
        print("Installing ROS1...")
        # run(["sudo", "apt-get", "update"])
        # run(["sudo", "apt-get", "install", "-y", "ros-noetic-desktop-full"])
    elif version == "2":
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
        run_command("sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg")
        run_command('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null')

        # install ros2 packages
        run_command("sudo apt update")
        run_command("sudo apt upgrade")
        run_command("sudo apt install ros-" + distribution + "python3-argcomplete")
        run_command("sudo apt install ros-dev-tools")

        # sourcing setup script

    print("ROS installation complete.")

def create_ros_project():
    pass


def main():

    install_ros = questionary.confirm("Do you need to install ROS?").ask()

    if install_ros:
        ros_version = questionary.select(
            "Which version of ROS would you like to install?",
            choices=['ROS 1', 'ROS 2'],
        ).ask()

        if(ros_version == 'ROS 1'):
            ros_distribution = questionary.select(
                "Which ROS 1 distribution would you like to install?",
                choices=['noetic', 'kinetic', 'melodic'],
            ).ask()
        else:
            ros_distribution = questionary.select(
                "Which ROS 2 distribution would you like to install?",
                choices=['galatic', 'foxy'],
            ).ask()

    project_name = questionary.txt(
        "What is your project named?"
    ).ask()

    project_language = questionary.select(
        "Would like to use ROS C++ or ROS Python?",
        choices=['C++', 'Python']
    ).ask()

    confirm_install = questionary.confirm(
        "Ok to proceed?", default=True
    ).ask()

    if confirm_install:
        install_ros(ros_version, ros_distribution)

if __name__ == "__main__":
    main()
