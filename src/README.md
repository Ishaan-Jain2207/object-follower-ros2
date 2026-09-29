# Object Follower Robot using ROS 2 Jazzy, SLAM, Nav2, and TurtleBot3 Simulation

A ROS 2 Jazzy simulation project that demonstrates autonomous robot simulation, SLAM-based mapping, Nav2 navigation, and vision-based object following using a TurtleBot3-style mobile robot.

## Project Overview

This project combines the following robotics capabilities:

- **ROS 2 Jazzy** for robot software integration
- **TurtleBot3 Simulation** for mobile robot simulation
- **Gazebo** for physics-based simulation
- **SLAM** for creating an occupancy-grid map of the environment
- **Nav2** for autonomous navigation and path planning
- **Object Tracking** for detecting and tracking a target object
- **Object Following** for commanding the robot to follow the tracked object

The project provides separate launch workflows for navigation, SLAM, and object tracking/following.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| ROS 2 Jazzy | Robot middleware and application framework |
| Gazebo | Robot and environment simulation |
| TurtleBot3 | Mobile robot simulation platform |
| SLAM | Mapping and localization |
| Nav2 | Autonomous navigation |
| ROS 2 TF | Coordinate-frame transformations |
| Object Tracking | Target detection and tracking |
| Python / ROS 2 Nodes | Robot control and application logic |

---

## Workspace Setup

After building the ROS 2 workspace, source the workspace before running the launch files:

```bash
source install/setup.bash
```

If the workspace has not been built yet:

```bash
colcon build
source install/setup.bash
```

---

# 1. Robot Navigation

This workflow launches the robot simulation and the navigation stack.

### Terminal 1 — Start Robot Simulation

```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2 — Start Navigation

Open a new terminal:

```bash
source install/setup.bash
ros2 launch robot_bringup robot_navigation.launch.py
```

### Navigation Workflow

```text
Robot Simulation
       │
       ▼
   Sensors / TF
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
   cmd_vel
       │
       ▼
   Mobile Robot
```

---

# 2. SLAM

This workflow launches the robot simulation together with the SLAM and navigation environment.

### Terminal 1 — Start Robot Simulation

```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

### Terminal 2 — Start SLAM Navigation

Open a new terminal:

```bash
source install/setup.bash
ros2 launch robot_bringup slam_navigation.launch.py
```

### SLAM Workflow

```text
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
   Occupancy Map
       │
       ▼
      Nav2
       │
       ▼
   Robot Motion
```

SLAM can be used to build a map of the simulated environment while the robot moves through it.

---

# 3. Object Tracking and Following

This workflow launches the object-tracking simulation and the object-following controller.

### Terminal 1 — Start Ball/Object Tracking Simulation

```bash
source install/setup.bash
ros2 launch robot_bringup ball_track_simulation.launch.py
```

### Terminal 2 — Start Object Following

Open a new terminal:

```bash
source install/setup.bash
ros2 launch robot_bringup object_follow.launch.py
```

> **Note:** The launch file is `object_follow.launch.py` with a single `.` before `launch.py`.

### Object Following Workflow

```text
Simulated Object
       │
       ▼
   Camera / Sensor
       │
       ▼
 Object Detection
       │
       ▼
 Object Tracking
       │
       ▼
Follow Controller
       │
       ▼
    cmd_vel
       │
       ▼
   TurtleBot3
```

The object-following system continuously uses the tracked object's position relative to the robot to generate motion commands.

---

# Launch Summary

| Feature | Terminal 1 | Terminal 2 |
|---|---|---|
| Robot Navigation | `robot_simulation.launch.py` | `robot_navigation.launch.py` |
| SLAM | `robot_simulation.launch.py` | `slam_navigation.launch.py` |
| Object Tracking & Following | `ball_track_simulation.launch.py` | `object_follow.launch.py` |

For every terminal:

```bash
source install/setup.bash
```

---

## Recommended Execution Order

### Navigation

**Terminal 1**
```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

**Terminal 2**
```bash
source install/setup.bash
ros2 launch robot_bringup robot_navigation.launch.py
```

### SLAM

**Terminal 1**
```bash
source install/setup.bash
ros2 launch robot_bringup robot_simulation.launch.py
```

**Terminal 2**
```bash
source install/setup.bash
ros2 launch robot_bringup slam_navigation.launch.py
```

### Object Following

**Terminal 1**
```bash
source install/setup.bash
ros2 launch robot_bringup ball_track_simulation.launch.py
```

**Terminal 2**
```bash
source install/setup.bash
ros2 launch robot_bringup object_follow.launch.py
```

---

## Project Architecture

```text
                    Object Follower Robot
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
          Gazebo          SLAM           Object
        Simulation       Mapping         Tracking
             │              │              │
             │              ▼              │
             │          Occupancy Map      │
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                           Nav2
                            │
                    Path Planning &
                    Motion Control
                            │
                            ▼
                         cmd_vel
                            │
                            ▼
                       TurtleBot3
```

---

## Package

Main bringup package:

```text
robot_bringup
```

Important launch files:

```text
robot_simulation.launch.py
robot_navigation.launch.py
slam_navigation.launch.py
ball_track_simulation.launch.py
object_follow.launch.py
```

---

## Requirements

Make sure the following are installed and configured:

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo compatible with ROS 2 Jazzy
- Nav2
- SLAM Toolbox
- TurtleBot3 simulation dependencies
- Required ROS 2 Python/C++ dependencies for the project

Verify ROS 2:

```bash
ros2 --version
```

Verify the package:

```bash
ros2 pkg list | grep robot_bringup
```

---

## Troubleshooting

### Package Not Found

If ROS 2 cannot find `robot_bringup`:

```bash
source install/setup.bash
```

If the package is still not found, rebuild the workspace:

```bash
colcon build
source install/setup.bash
```

### Launch File Not Found

Check available launch files:

```bash
ros2 pkg prefix robot_bringup
```

Then verify that the required launch files are installed in the package's share directory.

### Check ROS 2 Topics

```bash
ros2 topic list
```

### Check Active Nodes

```bash
ros2 node list
```

### Check TF

```bash
ros2 topic echo /tf
```

### Check Velocity Commands

```bash
ros2 topic echo /cmd_vel
```

---

## Project Goal

The main goal of this project is to demonstrate how a simulated mobile robot can combine:

**Simulation → Perception → Mapping → Localization → Navigation → Object Tracking → Object Following**

This provides a practical ROS 2 Jazzy foundation for developing more advanced autonomous mobile robot applications.

---

## Author

**Sampath**

Robotics Engineer
