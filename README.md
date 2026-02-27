# Project Vihang — Software & Simulation Layer

**Vihang** is a VTOL (Vertical Take-Off and Landing) aerial vehicle development project. The goal is to build a system that can take off vertically like a drone, transition into forward flight like a fixed-wing aircraft, and remain stable and controllable throughout.

This repository (`kaarthik` branch) contains the **software and simulation layer** of the project, built on top of ROS2 Humble, Gazebo, and ArduPilot.

---

## System Overview

Project Vihang spans four engineering domains working in parallel:

| Domain | Role |
|---|---|
| Mechanical | Airframe and structural design |
| Electrical | Sensors and power systems |
| Control | Stability and flight logic |
| **Software** | **Simulation, autonomy, and interface ← this repo** |

---

## What This Repository Covers

- **VTOL model setup** — URDF/SDF model of the vehicle configured for Gazebo simulation
- **Simulation environment** — World configuration and Gazebo scene setup for flight testing
- **ROS2 nodes and topics** — Communication layer between simulation components using ROS2 Humble
- **ArduPilot integration** — Flight stack connection with ArduPilot for realistic flight behavior in simulation

---

## Tech Stack

| Tool | Purpose |
|---|---|
| ROS2 Humble | Middleware and communication framework |
| Gazebo | Physics-based flight simulation |
| ArduPilot | Flight stack / autopilot |
| Python / C++ | Node logic and utilities |
| CMake / Makefile | Build system |

---

## Repository Structure

```
Vihang/
├── ros2_ws/        # ROS2 workspace
├── src/            # Source code — ROS2 packages and nodes
├── build/          # Build artifacts (auto-generated)
├── install/        # Install space (auto-generated)
├── log/            # ROS2 logs (auto-generated)
└── README.md
```

---

## Getting Started

### Prerequisites

- Ubuntu 22.04
- [ROS2 Humble](https://docs.ros.org/en/humble/Installation.html)
- [Gazebo](https://gazebosim.org/docs)
- [ArduPilot](https://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html) (SITL setup)

### Build

```bash
# Clone the repository
git clone -b kaarthik https://github.com/MUNDRAGARV/Vihang.git
cd Vihang/ros2_ws

# Source ROS2
source /opt/ros/humble/setup.bash

# Build the workspace
colcon build

# Source the workspace
source install/setup.bash
```

### Launch Simulation

```bash
ros2 launch <package_name> <launch_file>.launch.py
```

> Replace `<package_name>` and `<launch_file>` with the appropriate names from the `src/` directory.

---

## Team

This is a club project. The `kaarthik` branch represents the simulation and software contributions by **M Kaarthikeya**

For the full project, see the other branches of this repository.

---

## Acknowledgements

- [ArduPilot](https://ardupilot.org/)
- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Sim](https://gazebosim.org/)
