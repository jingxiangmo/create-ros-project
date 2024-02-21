# Create ROS Project (Under Development 🔨)

Getting started, setting up, and managing ROS dependencies is hard. CRP helps you install, setup, and manage your robotics projects with one command.

## Installation
```
git clone https://github.com/jingxiangmo/create-ros-project && cd create-ros-project && python3 setup.py install && python3 src/main.py
```
SOON WILL BE MADE INTO AN UBUNTU AND MAC PACKAGE!


## Roadmap
#### 1. ROS installer and project creator 

  A [create react app](https://create-react-app.dev) like developer experience for installing ROS and setting up a ROS project. 
  
  **Goals**
  - ROS installer that supports major ROS 1 and 2 distributions on Ubuntu and MacOS.
  - ROS system level dependency management.
  - Project templates.

#### 2. Gather feedback and improve installer & creator

Understand the ROS community needs and what could be improved.

#### 3. Packages manager [TBD]

A [Poetry](https://python-poetry.org) like developer experience for managing ROS packages.

#### 4. Model replacements and environment [TBD]

Make it easy to experiment and test out different perception, obstacle avoidance, and other machine learning models.


## Current Supports
(MORE SUPPORT COMING SOON! CRP currently support the most used ROS distribution and platform. Since this is a relatively new project, the current supports are for my current projects with my research teams and competition teams. If you have a specific version you would like to request, please let me know.)
#### ROS 1
- Neotic, Ubuntu 20.04 (arm64 and amd64)
- Melodic, Ubuntu 18.04.6 (arm 64 and amd64)

#### ROS 2
- Iron, Ubuntu 22.04 (arm 64 and amd64)
- Foxy, Ubuntu 20.04 (arm64 and amd64)


## Contribute
Please create PR or open up an issue. Thank you for your support!
