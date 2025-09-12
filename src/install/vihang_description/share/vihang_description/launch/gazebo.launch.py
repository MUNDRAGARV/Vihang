from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('vihang_description')
    urdf_file = os.path.join(pkg_path, 'urdf', 'vihang.urdf.xacro')

    return LaunchDescription([
        # Start Gazebo with ROS plugins
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Publish joint states from URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_file]
        ),

        # Spawn robot into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_vihang',
            output='screen',
            arguments=['-entity', 'vihang', '-file', urdf_file]
        ),
    ])
