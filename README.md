# Object Follower Robot — ROS 2 Jazzy

A ROS 2 Jazzy simulation project for a two-wheeled mobile robot integrating **Gazebo Harmonic, OpenCV-based object detection, object following, ROS 2 control, SLAM, and Nav2 navigation**.

The primary object-following workflow uses a simulated RGB camera to detect a colored target ball, publishes its normalized image position through `/detected_ball`, and generates velocity commands to move the robot toward the target.

<p align="center">
  <b>ROS 2 Jazzy</b> · <b>Gazebo Harmonic</b> · <b>OpenCV</b> · <b>SLAM Toolbox</b> · <b>Nav2</b> · <b>Python</b>
</p>

---

## Overview

The project is organized into separate ROS 2 packages for robot description, simulation, control, perception, and navigation.

The main object-following pipeline is:

```text
Gazebo Simulation
       │
       ▼
Simulated RGB Camera
       │
       ▼
OpenCV Image Processing
       │
       ▼
Colored Ball Detection
       │
       ▼
/detected_ball
       │
       ▼
Follow Ball Controller
       │
       ▼
/cmd_vel_tracker
       │
       ▼
twist_mux
       │
       ▼
Velocity Relay / Robot Controller
       │
       ▼
Mobile Robot
```

The repository also contains separate workflows for:

- Robot simulation
- Camera-based colored ball detection
- 2D ball detection and 3D ball estimation
- Object following
- Robot velocity control
- SLAM mapping
- Nav2 navigation
- Gazebo and RViz2 visualization

---

## System Architecture

### Object Following

```text
┌─────────────────────────┐
│    Gazebo Harmonic      │
│   Colored Shapes World  │
└────────────┬────────────┘
             │
             │ Camera Image
             ▼
┌─────────────────────────┐
│      detect_ball        │
│       OpenCV            │
│  Color / Shape Detection│
└────────────┬────────────┘
             │
             │ /detected_ball
             ▼
┌─────────────────────────┐
│      follow_ball        │
│  Target-based Control   │
└────────────┬────────────┘
             │
             │ /cmd_vel_tracker
             ▼
┌─────────────────────────┐
│       twist_mux         │
│   Command Multiplexing  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Velocity Relay /      │
│   Robot Controller      │
└────────────┬────────────┘
             │
             ▼
       Mobile Robot
```

The perception package also contains a `detect_ball_3d` node that consumes the 2D detection and publishes a 3D ball estimate and visualization marker.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **ROS 2 Jazzy** | Robotics middleware and node communication |
| **Gazebo Harmonic** | Robot and environment simulation |
| **Python** | ROS 2 nodes, perception and control logic |
| **OpenCV** | Image processing and colored-ball detection |
| **ros_gz_sim / ros_gz_bridge** | Gazebo–ROS 2 integration |
| **ROS 2 TF** | Coordinate-frame transformations |
| **SLAM Toolbox** | Simultaneous localization and mapping |
| **Nav2** | Autonomous navigation stack |
| **RViz2** | Robot, sensor and navigation visualization |

---

# Repository Structure

```text
object-follower-ros2/
├── README.md
├── .gitignore
├── docs/
│   └── media/
│       ├── object-detection.png
│       ├── robot-following.png
│       └── demo.mov
└── src/
    ├── robot_bringup/
    ├── robot_controller/
    ├── robot_description/
    ├── robot_navigation/
    └── robot_perception/
```

## ROS 2 Packages

| Package | Responsibility |
|---|---|
| `robot_bringup` | High-level launch files integrating simulation, control, perception and navigation workflows |
| `robot_controller` | Robot controller, velocity relay, command multiplexing and teleoperation configuration |
| `robot_description` | Robot URDF/Xacro, Gazebo worlds, sensors, RViz configuration and Gazebo–ROS bridge configuration |
| `robot_navigation` | SLAM, localization and Nav2 configuration |
| `robot_perception` | Ball detection, image processing, 3D estimation and object-following logic |

---

# Object Following

The main demonstration uses a **colored ball in the `colored_shapes` Gazebo world**.

The simulated camera provides an RGB image to the perception node. OpenCV processing identifies the target ball and publishes its normalized image position and size on:

```text
/detected_ball
```

The follower consumes this detection and produces velocity commands for the robot.

## Run the Object-Following Simulation

### Terminal 1 — Start simulation

From the workspace root:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_bringup ball_track_simulation.launch.py
```

This launch file starts the object-following simulation environment, robot controller, teleoperation components and RViz2.

### Terminal 2 — Start perception and following

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_perception perception.launch.py
```

This launches the perception pipeline containing:

```text
detect_ball
detect_ball_3d
follow_ball
```

---

## Object-Following Data Flow

```text
/camera/image_raw
        │
        ▼
   detect_ball
        │
        ├──────────────► /image_out
        │
        ▼
 /detected_ball
        │
        ├──────────────► detect_ball_3d
        │                       │
        │                       ├──► /detected_ball_3d
        │                       └──► /ball_3d_marker
        │
        ▼
   follow_ball
        │
        ▼
/cmd_vel_tracker
        │
        ▼
    twist_mux
        │
        ▼
  velocity relay
        │
        ▼
 robot controller
        │
        ▼
     Gazebo
```

---

# Perception

The `robot_perception` package contains the computer-vision components used by the object-following workflow.

### Main perception nodes

| Node | Function |
|---|---|
| `detect_ball` | Processes camera images and detects the target ball |
| `detect_ball_3d` | Estimates the ball's 3D position from the 2D detection and publishes a visualization marker |
| `follow_ball` | Generates robot velocity commands based on the detected ball |

The image-processing pipeline uses OpenCV and HSV-based color thresholding configured through:

```text
src/robot_perception/config/ball_tracker_params_sim.yaml
```

The simulation configuration contains color-tuning parameters for the target detection.

---

# SLAM

The repository contains a separate SLAM workflow for generating an occupancy-grid map of the simulated environment.

The navigation package includes configuration for:

- SLAM Toolbox
- AMCL/localization
- Nav2

### Run the SLAM workflow

### Terminal 1 — Start the robot simulation

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2 — Start SLAM/navigation integration

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_bringup slam_navigation.launch.py
```

### SLAM data flow

```text
LiDAR
  │
  ├──────────────┐
  │              │
  ▼              ▼
Sensor Data    Odometry / TF
       \        /
        \      /
         ▼    ▼
       SLAM Toolbox
            │
            ▼
     Occupancy Grid Map
```

---

# Nav2 Navigation

The repository also contains a separate Nav2 navigation workflow.

Navigation configuration is maintained in:

```text
src/robot_navigation/config/
```

including:

```text
nav2_params.yaml
amcl.yaml
slam_toolbox.yaml
```

### Run the navigation workflow

### Terminal 1 — Start the robot simulation

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2 — Start Nav2

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch robot_bringup robot_navigation.launch.py
```

The navigation workflow uses the configured Nav2 stack for autonomous navigation within the simulated environment.

---

# Build and Setup

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Python 3
- OpenCV
- `ros_gz_sim`
- `ros_gz_bridge`
- RViz2
- SLAM Toolbox
- Nav2
- `colcon`

## Clone the Repository

```bash
git clone https://github.com/Ishaan-Jain2207/object-follower-ros2.git
cd object-follower-ros2
```

## Build the Workspace

The ROS 2 workspace is located in:

```text
object_follower_ws/
```

Enter the workspace:

```bash
cd object_follower_ws
```

Source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Build:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

### Clean Build

If a clean rebuild is required:

```bash
rm -rf build install log
colcon build
source install/setup.bash
```

---

# Useful ROS 2 Commands

### List active nodes

```bash
ros2 node list
```

### List topics

```bash
ros2 topic list
```

### Inspect the detected ball

```bash
ros2 topic echo /detected_ball
```

### Inspect camera topics

```bash
ros2 topic list | grep camera
```

### Inspect velocity commands

```bash
ros2 topic echo /cmd_vel
```

### Inspect TF

```bash
ros2 topic echo /tf
```

### Inspect topic connections

```bash
ros2 topic info /detected_ball -v
```

---

# Launch Reference

| Workflow | Launch Command |
|---|---|
| General Robot Simulation | `ros2 launch robot_bringup robot_simulation.launch.py` |
| Object-Following Simulation | `ros2 launch robot_bringup ball_track_simulation.launch.py` |
| Perception & Object Following | `ros2 launch robot_perception perception.launch.py` |
| SLAM Workflow | `ros2 launch robot_bringup slam_navigation.launch.py` |
| Nav2 Navigation | `ros2 launch robot_bringup robot_navigation.launch.py` |

---

# Demo

The repository includes screenshots and a demonstration recording from the object-following simulation.

## Object Detection

![Object Detection](docs/media/object-detection.png)

## Robot Following

![Robot Following](docs/media/robot-following.png)

### Demonstration Video

The complete demonstration recording shows the simulated robot detecting the target ball and following it in Gazebo.

> **Demo video:** `demo.mov`

If the video is later hosted on YouTube, this section can be replaced with a clickable video thumbnail.

---

# Project Scope

This project brings together several core robotics components in a simulated ROS 2 environment:

- **Robot simulation** using Gazebo Harmonic
- **Computer vision** using OpenCV
- **Colored-object detection** from a simulated camera
- **2D object localization** using normalized image coordinates
- **3D target estimation**
- **Object-following control**
- **ROS 2 command multiplexing and velocity control**
- **SLAM mapping**
- **Nav2-based navigation**
- **RViz2 visualization**
- **ROS 2–Gazebo communication through `ros_gz_bridge`**

The object-following workflow and the SLAM/Nav2 workflows are implemented as separate launchable components within the same ROS 2 workspace.

---

## Author

**Ishaan Jain**

B.Tech Computer Science & Engineering — Data Science  
NMIMS Chandigarh
