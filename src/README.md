# Object Follower Robot using ROS 2 Jazzy

A ROS 2 Jazzy-based mobile robot simulation project demonstrating robot simulation, perception, object detection, object tracking, object following, SLAM-based mapping, and Nav2 navigation using Gazebo.

---

## Project Overview

This project combines multiple robotics capabilities:

- **ROS 2 Jazzy** for robot software integration
- **Gazebo** for physics-based robot simulation
- **Computer vision** for target object detection
- **Object tracking** for estimating the target position
- **Object following** for generating robot velocity commands
- **SLAM Toolbox** for mapping the simulated environment
- **Nav2** for autonomous navigation
- **ROS 2 TF** for coordinate-frame transformations
- **RViz2** for visualization and monitoring

The project is organized into separate ROS 2 packages for robot description, control, perception, navigation, and system bringup.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| ROS 2 Jazzy | Robot middleware and application framework |
| Gazebo | Robot and environment simulation |
| Python | Perception and robot application nodes |
| OpenCV | Image processing and object detection |
| SLAM Toolbox | Simultaneous localization and mapping |
| Nav2 | Autonomous navigation |
| ROS 2 TF | Coordinate-frame transformations |
| RViz2 | Visualization and monitoring |

---

## Project Structure

```text
object_follower_ws/
└── src/
    ├── robot_bringup/
    ├── robot_controller/
    ├── robot_description/
    ├── robot_navigation/
    └── robot_perception/
Main Packages
Package	Purpose
robot_bringup	Launch files and system integration
robot_controller	Robot motion and control functionality
robot_description	Robot model and simulation description
robot_navigation	Navigation, SLAM, and related configuration
robot_perception	Object detection, tracking, and following
1. Robot Navigation

This workflow launches the robot simulation and the navigation stack.

Terminal 1 — Start Robot Simulation
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
Terminal 2 — Start Navigation
source install/setup.bash
ros2 launch robot_bringup robot_navigation.launch.py
Navigation Workflow
Robot Simulation
       │
       ▼
 Sensors / Odometry / TF
       │
       ▼
      Nav2
       │
       ├── Global Planner
       ├── Local Controller
       ├── Costmaps
       └── Recovery Behaviors
       │
       ▼
 Velocity Commands
       │
       ▼
     Robot
2. SLAM

The SLAM workflow allows the simulated robot to build an occupancy-grid map while moving through the environment.

Terminal 1 — Start Robot Simulation
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
Terminal 2 — Start SLAM Navigation
source install/setup.bash
ros2 launch robot_bringup slam_navigation.launch.py
SLAM Workflow
Robot Simulation
       │
       ├── LiDAR / Sensors
       ├── Odometry
       └── TF
       │
       ▼
     SLAM
       │
       ▼
 Occupancy Grid Map
       │
       ▼
      Nav2
       │
       ▼
 Robot Motion

SLAM can be used to build a map of the simulated environment while the robot moves through it.

3. Object Detection and Following

This workflow launches the dedicated object-tracking simulation and perception system.

Terminal 1 — Start Object Tracking Simulation
source install/setup.bash
ros2 launch robot_bringup ball_track_simulation.launch.py
Terminal 2 — Start Perception and Following
source install/setup.bash
ros2 launch robot_perception perception.launch.py

The perception launch file starts the object detection, object processing, and object-following nodes.

Object Following Workflow
Simulated Target Object
          │
          ▼
       Camera
          │
          ▼
   Image Processing
          │
          ▼
   Object Detection
          │
          ▼
   Object Position
          │
          ▼
   Follow Controller
          │
          ▼
    Velocity Commands
          │
          ▼
        Robot

The object-following system continuously uses the detected target's position relative to the robot to generate motion commands.

Launch Summary
Feature	Terminal 1	Terminal 2
Robot Navigation	robot_simulation.launch.py	robot_navigation.launch.py
SLAM	robot_simulation.launch.py	slam_navigation.launch.py
Object Detection & Following	ball_track_simulation.launch.py	perception.launch.py

For every terminal, source the workspace before running the launch file:

source install/setup.bash
Building the Workspace

From the workspace root:

colcon build

After building:

source install/setup.bash

For a clean rebuild:

rm -rf build install log
colcon build
source install/setup.bash
Requirements

The project is intended for:

Ubuntu 24.04
ROS 2 Jazzy
Gazebo compatible with ROS 2 Jazzy
Nav2
SLAM Toolbox
RViz2
Required ROS 2 Python and simulation dependencies

Verify ROS 2 installation:

ros2 --version

Verify the main bringup package:

ros2 pkg list | grep robot_bringup
Useful ROS 2 Commands
List ROS 2 Topics
ros2 topic list
List Active Nodes
ros2 node list
Check Detected Object
ros2 topic echo /detected_ball
Check Camera Topics
ros2 topic list | grep camera
Check Velocity Commands
ros2 topic echo /cmd_vel
Inspect TF
ros2 topic echo /tf
Project Architecture
                     Object Follower Robot
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
       Gazebo                SLAM             Perception
     Simulation             Mapping           & Detection
          │                   │                   │
          │                   ▼                   ▼
          │              Occupancy Map      Object Position
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                       Robot Controller
                              │
                              ▼
                      Velocity Commands
                              │
                              ▼
                           Robot
Main Launch Files

The main bringup launch files are located in:

robot_bringup/launch/

Important launch files:

robot_simulation.launch.py
robot_navigation.launch.py
slam_navigation.launch.py
ball_track_simulation.launch.py

The object perception workflow is launched from:

robot_perception/launch/perception.launch.py
Perception Pipeline

The object-following system uses a simulated camera feed for perception.

The camera image is processed to identify the target object. The detected target position is published through:

/detected_ball

The follow controller uses the detected target information to generate velocity commands for the robot.

The processed camera output can also be visualized using ROS 2 image visualization tools and RViz2.

Development Notes

The project is designed as a simulation-based robotics environment for experimenting with:

Robot simulation
Computer vision
Object detection
Object tracking
Robot control
SLAM
Autonomous navigation
ROS 2 system integration

The modular package structure allows individual components to be developed and tested independently.

Project Goal

The main goal of this project is to demonstrate a practical ROS 2 autonomous mobile robot workflow combining:

Simulation
     ↓
Perception
     ↓
Object Detection
     ↓
Object Tracking
     ↓
Robot Control
     ↓
Object Following

The project also provides separate SLAM and Nav2 workflows for exploring autonomous mobile robot navigation.

Author

Ishaan Jain

B.Tech Computer Science and Engineering (Data Science)

NMIMS Chandigarh
