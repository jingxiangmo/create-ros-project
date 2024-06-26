# Create ROS Project

Getting started, setting up, and managing ROS dependencies is hard. CRP helps you install, setup, and manage your robotics projects with one command.

<p align="center">
  <img src="https://cln.sh/xtYr5V8D/download" alt="CRP video"/>
</p>

## Installation

Build from source:

```bash
git clone https://github.com/jingxiangmo/create-ros-project && cd create-ros-project && go build .
```

## Usage

Simply run the app from a terminal and answer the prompts. Arrow keys and enter
work as expected.

```bash
# from folder containing the executable
./create-ros-project

# if in PATH
create-ros-project
```

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


## Possible Future Features

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


## Contribute

Please create PR or open up an issue. Thank you for your support!
