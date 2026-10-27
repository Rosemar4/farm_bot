# farm_bot

![Farm bot simulation](https://github.com/user-attachments/assets/e417cf81-365e-42d7-9247-a38cca036478)

A ROS 2 package for a farm robot simulated in Gazebo (Ignition). The robot drives through a farm world and uses LiDAR-based obstacle avoidance to move around obstacles.

## Features

- Farm world simulation in Gazebo (`worlds/farm_world.sdf`)
- Robot model defined with xacro (`urdf/farm_bot.xacro`)
- Reactive obstacle avoidance using LiDAR scan data (`farm_bot/obstacle_avoidance.py`)
- Single launch file that starts the simulation, robot, bridges, and controller

## Requirements

- ROS 2 (Humble or newer) on Ubuntu 22.04
- Gazebo (Ignition / `ros_gz`)
- Python packages: `rclpy`, `xacro`
- ROS packages: `robot_state_publisher`, `ros_gz_sim`, `ros_gz_bridge`, `sensor_msgs`, `geometry_msgs`

## Installation

Create a colcon workspace and clone the repo into its `src` folder:

```bash
mkdir -p ~/farm_ws/src
cd ~/farm_ws/src
git clone https://github.com/Rosemar4/farm_bot.git
```

Install dependencies from the workspace root:

```bash
cd ~/farm_ws
rosdep install --from-paths src --ignore-src -r -y
```

Build the package:

```bash
colcon build --packages-select farm_bot
source install/setup.bash
```

## Usage

Launch the simulation, robot, and obstacle avoidance node:

```bash
ros2 launch farm_bot farm_bot.launch.py
```

The robot starts at (0, 0, 0.2) and moves forward until it detects an obstacle within 1.0 m in front of it, then turns toward the side with more open space.

## Package Structure

## Parameters

Tunable values are set in `farm_bot/obstacle_avoidance.py`:

| Parameter       | Default   | Description                               |
|-----------------|-----------|-------------------------------------------|
| `safe_distance` | 1.0 m     | Distance at which the robot stops/turns   |
| `linear_speed`  | 0.5 m/s   | Forward speed when the path is clear      |
| `angular_speed` | 0.8 rad/s | Turning speed when avoiding an obstacle   |

## Troubleshooting

- **`Package 'farm_bot' not found`**: run `source install/setup.bash` after building.
- **No `/scan` data**: check that the LiDAR is defined in `farm_bot.xacro` and that the bridge is running (`ros2 topic list`).
- **Robot doesn't move**: confirm `/cmd_vel` is bridged with `ros2 topic echo /cmd_vel`.

## License

Apache License 2.0. See `setup.py` for details.

## Maintainer

Rosemary Ojoawo (rbojoawo@student.lautech.edu.ng)
