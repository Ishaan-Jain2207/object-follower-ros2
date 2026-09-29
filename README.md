
# Object Follower Robot — ROS 2 Jazzy

A ROS 2 Jazzy-based autonomous mobile robot simulation project integrating **Gazebo, Computer Vision, Object Detection, Object Following, SLAM, and Nav2**.

The primary objective is to detect a target object using a simulated camera and control the robot to follow the detected target in a simulated environment.

<p align="center">
  <b>ROS 2 Jazzy</b> · <b>Gazebo</b> · <b>OpenCV</b> · <b>SLAM</b> · <b>Nav2</b> · <b>Python</b>
</p>

---

## Overview

This project explores a complete ROS 2 mobile robotics workflow:

**Simulation → Perception → Object Detection → Tracking → Robot Control → Object Following**

The system includes separate workflows for:

- 🤖 Robot simulation
- 👁️ Camera-based object detection
- 🎯 Object tracking and following
- 🗺️ SLAM-based mapping
- 🧭 Nav2 autonomous navigation
- 📡 ROS 2 topic and TF communication
- 📊 Gazebo and RViz2 visualization

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │   Gazebo Simulation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Camera / Sensors  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Object Detection  │
                    │      OpenCV         │
                    └──────────┬──────────┘
                               │
                               │ /detected_ball
                               ▼
                    ┌─────────────────────┐
                    │  Follow Controller  │
                    └──────────┬──────────┘
                               │
                               │ Velocity Commands
                               ▼
                    ┌─────────────────────┐
                    │   Robot Controller  │
                    └──────────┬──────────┘
                               │
                               ▼
                         Mobile Robot
````

---

## Technology Stack

| Technology       | Role                                         |
| ---------------- | -------------------------------------------- |
| **ROS 2 Jazzy**  | Robotics middleware                          |
| **Gazebo**       | Robot and environment simulation             |
| **Python**       | ROS 2 nodes and application logic            |
| **OpenCV**       | Camera image processing and object detection |
| **SLAM Toolbox** | Mapping and localization                     |
| **Nav2**         | Autonomous navigation                        |
| **RViz2**        | Visualization                                |
| **ROS 2 TF**     | Coordinate transformations                   |

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
```

### Packages

| Package             | Description                              |
| ------------------- | ---------------------------------------- |
| `robot_bringup`     | System integration and launch files      |
| `robot_controller`  | Robot motion and control                 |
| `robot_description` | Robot model and simulation configuration |
| `robot_navigation`  | Navigation and SLAM configuration        |
| `robot_perception`  | Object detection, tracking and following |

---

# Object Following

The main workflow uses a simulated camera to detect a target object and generate motion commands that allow the robot to follow it.

### Launch

**Terminal 1 — Start the simulation**

```bash
source install/setup.bash
ros2 launch robot_bringup ball_track_simulation.launch.py
```

**Terminal 2 — Start perception and following**

```bash
source install/setup.bash
ros2 launch robot_perception perception.launch.py
```

### Perception Pipeline

```text
Camera Image
     │
     ▼
OpenCV Processing
     │
     ▼
Object Detection
     │
     ▼
/detected_ball
     │
     ▼
Follow Controller
     │
     ▼
Velocity Command
     │
     ▼
Robot
```

The detected object position is published through:

```text
/detected_ball
```

---

# SLAM

The project also provides a SLAM workflow for building an occupancy-grid map of the simulated environment.

### Terminal 1

```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2

```bash
source install/setup.bash
ros2 launch robot_bringup slam_navigation.launch.py
```

### SLAM Pipeline

```text
LiDAR + Odometry + TF
          │
          ▼
     SLAM Toolbox
          │
          ▼
   Occupancy Grid Map
          │
          ▼
         Nav2
```

---

# Nav2 Navigation

The navigation workflow launches the robot simulation together with the Nav2 navigation stack.

### Terminal 1

```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2

```bash
source install/setup.bash
ros2 launch robot_bringup robot_navigation.launch.py
```

Nav2 provides the navigation components required for planning and controlling robot motion in the simulated environment.

---

# Build the Workspace

Clone the repository and enter the workspace:

```bash
cd object_follower_ws
```

Build the packages:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

For a clean rebuild:

```bash
rm -rf build install log
colcon build
source install/setup.bash
```

---

# Requirements

* Ubuntu 24.04
* ROS 2 Jazzy
* Gazebo
* Nav2
* SLAM Toolbox
* RViz2
* OpenCV
* Required ROS 2 dependencies

Verify ROS 2:

```bash
ros2 --version
```

Verify the project package:

```bash
ros2 pkg list | grep robot_bringup
```

---

# Useful Commands

### List active nodes

```bash
ros2 node list
```

### List available topics

```bash
ros2 topic list
```

### Monitor detected object

```bash
ros2 topic echo /detected_ball
```

### Monitor camera topics

```bash
ros2 topic list | grep camera
```

### Monitor velocity commands

```bash
ros2 topic echo /cmd_vel
```

### Inspect TF

```bash
ros2 topic echo /tf
```

---

# Launch Reference

| Workflow                    | Launch Command                                              |
| --------------------------- | ----------------------------------------------------------- |
| Robot Simulation            | `ros2 launch robot_bringup robot_simulation.launch.py`      |
| Navigation                  | `ros2 launch robot_bringup robot_navigation.launch.py`      |
| SLAM                        | `ros2 launch robot_bringup slam_navigation.launch.py`       |
| Object Following Simulation | `ros2 launch robot_bringup ball_track_simulation.launch.py` |
| Perception & Following      | `ros2 launch robot_perception perception.launch.py`         |

---

## Project Goals

This project serves as a practical ROS 2 simulation environment for exploring:

* Mobile robot simulation
* Computer vision
* Object detection
* Object tracking
* Robot control
* SLAM
* Autonomous navigation
* ROS 2 system integration

It provides a foundation for extending the system toward more advanced autonomous robotics and perception applications.

---

## Author

**Ishaan Jain**

B.Tech Computer Science & Engineering — Data Science
NMIMS Chandigarh

```
```
