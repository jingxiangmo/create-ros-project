from utils import *

"""
NOTE: Installation scripts are provided by the official documentation. For safety reasons, the commands should NOT be  
different from the official documentation. 
If you see any mistakes or differences. Please open a Github Issue immediately.

ROS 1:
Noetic Ninjemys: http://wiki.ros.org/noetic/Installation/Ubuntu
Foxy Fitzroy: https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html

ROS 2:
Iron Irwini:https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html
Foxy Fitzroy: https://docs.ros.org/en/foxy/Installation/Alternatives/Ubuntu-Development-Setup.html
"""


def run_ros_install(ros_version, ros_distribution):
    distributions = {
        "ROS 1 Noetic": "noetic",
        "ROS 1 Melodic": "melodic",

        "ROS 2 Iron": "iron",
        "ROS 2 Foxy": "foxy"
    }

    ros_distribution = distributions[ros_distribution]

    if ros_version == "1":
        print("Installing ROS1...")

        # setup sources.list
        run_command(
            """sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' """)

        # set up keys
        run_command("sudo apt install curl")
        run_command("curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -")

        # installation
        run_command("sudo apt update")
        run_command("sudo apt install ros-" + ros_distribution + "-desktop-full")

        # environment setup
        run_command("source /opt/ros/" + ros_distribution + "/setup.bash >> ~/.bashrc")
        run_command("source ~/.bashrc")

        # dependencies for building packages
        run_command(
            "sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential")

        # initialize rosdep
        run_command("sudo apt install python3-rosdep")
        run_command("sudo rosdep init")
        run_command("rosdep update")


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
        run_command("sudo apt install ros-" + ros_distribution + " python3-argcomplete")
        run_command("sudo apt install ros-dev-tools")

        # environment setup
        run_command("source /opt/ros/" + ros_distribution + "/setup.bash")

    print("ROS installation complete.")
