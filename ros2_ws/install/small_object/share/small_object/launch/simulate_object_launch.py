import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = get_package_share_directory('small_object')
    world_file = os.path.join(pkg_share, 'worlds', 'simple.world')
    model_file = os.path.join(pkg_share, 'sdf', 'cube.sdf')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Launch Gazebo with world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])]),
        launch_arguments={'gz_args': world_file}.items()
    )

    # Spawn the object
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'small_cube',
            '-file', model_file,
            '-x', '0.0', '-y', '0.0', '-z', '1.0'  # Optional: spawn 1m above ground
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn,
    ])