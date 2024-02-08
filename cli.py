import questionary
from subprocess import run
import os

def install_ros(version, distribution):
    if version == "1":
        print("Installing ROS1...")
        # run(["sudo", "apt-get", "update"])
        # run(["sudo", "apt-get", "install", "-y", "ros-noetic-desktop-full"])
    elif version == "2":
        print("Installing ROS2...")
        # run(["sudo", "apt-get", "update"])
        # run(["sudo", "apt-get", "install", "-y", "ros-foxy-desktop"])
    print("ROS installation complete.")


def main():
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

    confirm_install = questionary.confirm(
        "Ok to proceed?", default=True
    ).ask()

    if confirm_install:
        install_ros(ros_version, ros_distribution)

if __name__ == "__main__":
    main()
