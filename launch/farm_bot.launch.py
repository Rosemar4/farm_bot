import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    
    # Package directories
    pkg_name = 'farm_bot'
    pkg_dir = get_package_share_directory(pkg_name)
    
    # Paths
    urdf_file = os.path.join(pkg_dir, 'urdf', 'farm_bot.xacro')
    world_file = os.path.join(pkg_dir, 'worlds', 'farm_world.sdf')
    
    # Process xacro to get URDF
    robot_description = xacro.process_file(urdf_file).toxml()
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )
    
    # Gazebo launch
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', world_file, '-r'],
        output='screen'
    )
    
    # Spawn robot in Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'farm_bot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2'
        ],
        output='screen'
    )
    
    # Bridge for cmd_vel
    bridge_cmd_vel = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist'
        ],
        output='screen'
    )
    
    # Bridge for LiDAR
    bridge_scan = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan'
        ],
        output='screen'
    )
    
    # Bridge for odometry
    bridge_odom = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry'
        ],
        output='screen'
    )
    
    # Obstacle Avoidance Node
    obstacle_avoidance = Node(
        package='farm_bot',
        executable='obstacle_avoidance',
        name='obstacle_avoidance',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge_cmd_vel,
        bridge_scan,
        bridge_odom,
        obstacle_avoidance
    ])