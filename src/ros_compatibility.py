ros1_compatibility_map = {
    ('amd64', 'Ubuntu 20.04'): ['ROS 1 Noetic'],
    ('arm64', 'Ubuntu 20.04'): ['ROS 1 Noetic'],
    ('amd64', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
    ('armhf', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
    ('arm64', 'Ubuntu 18.04.6'): ['ROS 1 Melodic'],
    ('amd64', 'Ubuntu 17.10'): ['ROS 1 Melodic'],
}

ros2_compatibility_map = {
    ('amd64', 'Ubuntu 20.04'): ['ROS 2 Foxy'],
    ('arm64', 'Ubuntu 20.04'): ['ROS 2 Foxy'],
    ('arm32', 'Ubuntu 20.04'): ['ROS 2 Foxy '],
    ('amd64', 'Ubuntu 22.04'): ['ROS 2 Iron'],
    ('arm64', 'Ubuntu 22.04'): ['ROS 2 Iron'],
    ('amd64', 'macOS'): ['ROS 2 Iron'],
    ('amd64', 'macOS 10.14'): ['ROS 2 Foxy'],
}

def ros_compatibility(ros_version, architecture_type, os_type):
    if ros_version == "ROS 1":
        return ros1_compatibility_map.get((architecture_type, os_type), [])
    if ros_version == "ROS 2":
        return ros2_compatibility_map.get((architecture_type, os_type), [])
