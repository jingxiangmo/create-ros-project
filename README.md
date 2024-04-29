# Create ROS Project (WIP 🔨)

Getting started, setting up, and managing ROS dependencies is hard. CRP helps you install, setup, and manage your robotics projects with one command.

## Why Golang?

We want to have a trivial install process and a single command to run to get a
working ROS environment. Golang makes this easy, as the go compiler [outputs a
single, standalone executable with no system
dependencies](https://go.dev/solutions/clis#key-benefits). This includes system
libraries, so we don't need to worry about where libc is on a given linux
machine for example (different distributions put it in different places). Go
can also be compiled for many operating systems and architectures, including
everything ROS runs on. A single standalone executable means that all any
automated install has to do is grab the executable from where releases are
hosted for the appropriate platform, and put it somewhere reasonable on the
system (in PATH). That's it. In fact its so easy that anyone can do it
themselves just downloading the executable and dropping it in their PATH.

Additionally, go has a rich ecosystem of libraries and utilities just for
writing command line applications like ours. e.g.
[charm](https://charm.sh/libs/). Many important CLI applications leverage go
and its ecosystem such as the github CLI and lazygit.

Finally, go is designed to be extremely simplex (opposite of complex). We can
build what we need to with satisfactory technical properties and move on with our
lives. Alternatives such as rust and c++ share potentially similar desirable
technical properties and CLI ecosystems, but come with enormous complexity.

### Why not python?

Python introduces at the very least a dependency on python itself (and probably
a limited range of python versions because they break their standard library
disturbingly often) and also any libraries we use. More dependencies complicates
installation and development.

## Installation
```
git clone https://github.com/jingxiangmo/create-ros-project && cd create-ros-project && sudo python3 setup.py install && python3 src/main.py
```

## Features

Config file and flags. If people want to specify defaults they need from the CLI
up front, then they can pass a flag or set something in the config file.

E.g. if they do the same thing with create-ros-project every time why not just
write it down somewhere like a config file. Flags can be used to override things
e.g. if they want to keep stuff in the config file except one tiny change for one
run only, then pass a flag for that change.

To this end, the go version is a
[cobra](https://github.com/spf13/cobra?tab=readme-ov-file) and
[viper](https://github.com/spf13/viper) project. Cobra is a framework for making
CLI apps and parsing out flags and arguments, and viper is a config file parser.

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

~~- Neotic, Ubuntu 20.04 (arm64 and amd64)~~

~~- Melodic, Ubuntu 18.04.6 (arm 64 and amd64)~~

#### ROS 2
~~- Iron, Ubuntu 22.04 (arm 64 and amd64)~~
- Foxy, Ubuntu 20.04 (arm64 and amd64)


## Contribute
Please create PR or open up an issue. Thank you for your support!
