from utils import *


def run_ros_install(ros_version, ros_distribution):
    if ros_version == "1":
        print("Installing ROS1...")
        # run(["sudo", "apt-get", "update"])
        # run(["sudo", "apt-get", "install", "-y", "ros-noetic-desktop-full"])

    elif ros_version == "2":
        print("Installing ROS2...")

        # set locale
        run_command("locale")  # check for UTF-8

        run_command("sudo apt update && sudo apt install locales")
        run_command("sudo locale-gen en_US en_US.UTF-8")
        run_command("sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8")
        run_command("export LANG=en_US.UTF-8")

        run_command("locale")  # verify settings

        # setup sources
        run_command("sudo apt install software-properties-common")
        run_command("sudo add-apt-repository universe")

        # enable ubuntu universe repository
        run_command("sudo apt update && sudo apt install curl -y")

        # add ROS 2 GPG key with apt
        run_command(
            "sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg")

        # add repository to source list
        run_command(
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null')

        # install ros2 packages
        run_command("sudo apt update")
        run_command("sudo apt upgrade")
        run_command("sudo apt install ros-" + ros_distribution + "python3-argcomplete")
        run_command("sudo apt install ros-dev-tools")

    print("ROS installation complete.")
