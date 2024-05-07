echo "Installing ROS1..."

# setup sources.list

sudo echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list

# set up keys
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# installation
sudo apt update
sudo apt install "ros-$CRP_ROSDISTRO-desktop-full"

# environment setup
cat "/opt/ros/$CRP_ROSDISTRO/setup.bash" >> ~/.bashrc
source ~/.bashrc

# dependencies for building packages
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential

# initialize rosdep
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
