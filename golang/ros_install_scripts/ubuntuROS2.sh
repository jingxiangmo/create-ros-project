echo "Installing ROS2..."
echo "Setting locale..."

locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

# setup sources
echo "Setting setup sources..."
sudo apt install software-properties-common
sudo add-apt-repository universe

# enable ubuntu universe repository
echo "Enabling ubuntu universe repository..."
sudo apt update && sudo apt install curl -y

# add ROS 2 GPG key with apt
echo "Adding ROS 2 GPG key with apt..."
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# add repository to source list
echo "Adding repository to source list..."

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# install ros2 packages
echo "Installing ROS2 package..."
sudo apt update
sudo apt upgrade
sudo apt install "ros-$CRP_ROSDISTRO-desktop" python3-argcomplete
sudo apt install ros-dev-tools

# environment setup
#print("Setting up environment...")

echo "ROS installation complete. Please source /opt/ros/$CRP_ROSDISTRO/setup.bash"
