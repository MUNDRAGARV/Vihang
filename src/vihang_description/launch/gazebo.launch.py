#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():
    """
    Launch file for tilt_drone with ros2_control integration
    
    ASSUMPTIONS MADE (change these if different):
    - Package name: 'tilt_drone'
    - URDF file: 'urdf/tilt_drone.urdf.xacro' 
    - World file: 'worlds/empty.sdf'
    - Controller config: 'config/tilt_rotor_controllers.yaml' (optional, can use inline)
    - Joint names: left_front_tilt_joint, left_rear_tilt_joint, right_front_tilt_joint, right_rear_tilt_joint
    - Joint names: left_front_prop_joint, left_rear_prop_joint, right_front_prop_joint, right_rear_prop_joint
    """
    
    # ============================================================================
    # PACKAGE AND FILE PATHS
    # ============================================================================
    
    # Get package directory - ASSUMES package name is 'tilt_drone'
    pkg_tilt_drone = get_package_share_directory('tilt_drone')
    
    # URDF file path - ASSUMES URDF file is named 'tilt_drone.urdf.xacro'
    urdf_file = os.path.join(pkg_tilt_drone, 'urdf', 'tilt_drone.urdf.xacro')
    
    # Controller config file path - ASSUMES config file exists (optional, using inline config as backup)
    controller_config_file = os.path.join(pkg_tilt_drone, 'config', 'tilt_rotor_controllers.yaml')
    
    # World file paths - ASSUMES world file is named 'empty.sdf'
    custom_world_file = os.path.join(pkg_tilt_drone, 'worlds', 'empty.sdf')
    default_world_file = 'empty.sdf'  # Fallback to default Gazebo world
    
    # Choose world file (custom if exists, otherwise default)
    if os.path.exists(custom_world_file):
        world_file = custom_world_file
    else:
        world_file = default_world_file
    
    # ============================================================================
    # LAUNCH ARGUMENTS
    # ============================================================================
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')
    headless = LaunchConfiguration('headless')
    use_joystick = LaunchConfiguration('use_joystick')
    use_external_config = LaunchConfiguration('use_external_config')
    
    # Declare launch arguments with descriptions
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=world_file,
        description='Full path to world model file to load'
    )
    
    declare_gui_cmd = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Set to "false" to run headless.'
    )
    
    declare_headless_cmd = DeclareLaunchArgument(
        'headless',
        default_value='false',
        description='Set to "true" to run headless.'
    )
    
    declare_use_joystick_cmd = DeclareLaunchArgument(
        'use_joystick',
        default_value='true',
        description='Set to "true" to enable joystick control'
    )
    
    declare_use_external_config_cmd = DeclareLaunchArgument(
        'use_external_config',
        default_value='false',
        description='Set to "true" to use external controller config file'
    )

    # ============================================================================
    # GAZEBO SIMULATION
    # ============================================================================
    
    # Start Gazebo with GUI
    start_gazebo_cmd = ExecuteProcess(
        cmd=['gz', 'sim', world, '-v', '3'],
        output='screen',
        condition=IfCondition(gui)
    )
    
    # Start Gazebo headless (no GUI)
    start_gazebo_headless_cmd = ExecuteProcess(
        cmd=['gz', 'sim', world, '--headless-rendering', '-v', '3'],
        output='screen',
        condition=IfCondition(headless)
    )

    # ============================================================================
    # ROBOT DESCRIPTION AND STATE PUBLISHER
    # ============================================================================
    
    # Robot State Publisher - publishes robot description and transforms
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', urdf_file])  # Process URDF with xacro
        }]
    )

    # ============================================================================
    # ROS2 CONTROL CONFIGURATION
    # ============================================================================
    
    # INLINE CONTROLLER CONFIGURATION
    # ASSUMES joint names: *_tilt_joint and *_prop_joint
    # Change these joint names if your URDF uses different names
    inline_controller_config = {
        'controller_manager': {
            'ros__parameters': {
                'update_rate': 100,  # 100Hz control loop
                
                # Joint State Broadcaster - publishes all joint states
                'joint_state_broadcaster': {
                    'type': 'joint_state_broadcaster/JointStateBroadcaster'
                },
                
                # Individual Tilt Controllers (Position Control)
                'left_front_tilt_controller': {
                    'type': 'position_controllers/JointPositionController'
                },
                'left_rear_tilt_controller': {
                    'type': 'position_controllers/JointPositionController'
                },
                'right_front_tilt_controller': {
                    'type': 'position_controllers/JointPositionController'
                },
                'right_rear_tilt_controller': {
                    'type': 'position_controllers/JointPositionController'
                },
                
                # Individual Propeller Controllers (Velocity Control)
                'left_front_prop_controller': {
                    'type': 'velocity_controllers/JointVelocityController'
                },
                'left_rear_prop_controller': {
                    'type': 'velocity_controllers/JointVelocityController'
                },
                'right_front_prop_controller': {
                    'type': 'velocity_controllers/JointVelocityController'
                },
                'right_rear_prop_controller': {
                    'type': 'velocity_controllers/JointVelocityController'
                }
            }
        },
        
        # Individual Controller Parameters
        # TILT CONTROLLERS - Position control for precise angle control
        'left_front_tilt_controller': {
            'ros__parameters': {
                'joint': 'left_front_tilt_joint',  # ASSUMES this joint name in URDF
                'command_interfaces': ['position'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'left_rear_tilt_controller': {
            'ros__parameters': {
                'joint': 'left_rear_tilt_joint',   # ASSUMES this joint name in URDF
                'command_interfaces': ['position'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'right_front_tilt_controller': {
            'ros__parameters': {
                'joint': 'right_front_tilt_joint', # ASSUMES this joint name in URDF
                'command_interfaces': ['position'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'right_rear_tilt_controller': {
            'ros__parameters': {
                'joint': 'right_rear_tilt_joint',  # ASSUMES this joint name in URDF
                'command_interfaces': ['position'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        
        # PROPELLER CONTROLLERS - Velocity control for thrust/RPM control
        'left_front_prop_controller': {
            'ros__parameters': {
                'joint': 'left_front_prop_joint',  # ASSUMES this joint name in URDF
                'command_interfaces': ['velocity'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'left_rear_prop_controller': {
            'ros__parameters': {
                'joint': 'left_rear_prop_joint',   # ASSUMES this joint name in URDF
                'command_interfaces': ['velocity'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'right_front_prop_controller': {
            'ros__parameters': {
                'joint': 'right_front_prop_joint', # ASSUMES this joint name in URDF
                'command_interfaces': ['velocity'],
                'state_interfaces': ['position', 'velocity']
            }
        },
        'right_rear_prop_controller': {
            'ros__parameters': {
                'joint': 'right_rear_prop_joint',  # ASSUMES this joint name in URDF
                'command_interfaces': ['velocity'],
                'state_interfaces': ['position', 'velocity']
            }
        }
    }

    # ============================================================================
    # CONTROLLER MANAGER
    # ============================================================================
    
    # Controller Manager Node - manages all controllers
    # Uses inline config by default, can switch to external file
    controller_params = [{'use_sim_time': use_sim_time}]
    
    # Add controller configuration (inline or external file)
    if os.path.exists(controller_config_file):
        # Use external config file if it exists
        controller_params.append(controller_config_file)
    else:
        # Use inline configuration as fallback
        controller_params.append(inline_controller_config)
    
    controller_manager_cmd = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        output='screen',
        parameters=controller_params
    )

    # ============================================================================
    # CONTROLLER SPAWNERS
    # ============================================================================
    
    # Joint State Broadcaster Spawner - MUST be started first
    joint_state_broadcaster_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_state_broadcaster_spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # Tilt Controller Spawners - Position controllers for tilt joints
    left_front_tilt_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='left_front_tilt_controller_spawner',
        arguments=['left_front_tilt_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    left_rear_tilt_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='left_rear_tilt_controller_spawner',
        arguments=['left_rear_tilt_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    right_front_tilt_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='right_front_tilt_controller_spawner',
        arguments=['right_front_tilt_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    right_rear_tilt_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='right_rear_tilt_controller_spawner',
        arguments=['right_rear_tilt_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # Propeller Controller Spawners - Velocity controllers for propeller joints
    left_front_prop_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='left_front_prop_controller_spawner',
        arguments=['left_front_prop_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    left_rear_prop_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='left_rear_prop_controller_spawner',
        arguments=['left_rear_prop_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    right_front_prop_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='right_front_prop_controller_spawner',
        arguments=['right_front_prop_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    right_rear_prop_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        name='right_rear_prop_controller_spawner',
        arguments=['right_rear_prop_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # ============================================================================
    # ROS-GAZEBO BRIDGE
    # ============================================================================
    
    # Bridge for essential topics between ROS2 and Gazebo
    bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',           # Simulation time
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',             # Transform data
            '/tf_static@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',      # Static transforms
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # ============================================================================
    # ROBOT SPAWNING
    # ============================================================================
    
    # Spawn Robot in Gazebo
    spawn_robot_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_tilt_drone',
        arguments=[
            '-entity', 'tilt_drone',      # Robot name in simulation
            '-topic', 'robot_description', # Topic containing robot description
            '-x', '0.0',                  # Initial X position
            '-y', '0.0',                  # Initial Y position
            '-z', '0.5'                   # Initial Z position (0.5m above ground)
        ],
        output='screen'
    )

    # ============================================================================
    # JOYSTICK CONTROL (OPTIONAL)
    # ============================================================================
    
    # Joystick Node - reads joystick input
    joystick_cmd = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(use_joystick)
    )
    
    # Tilt Rotor Joystick Controller - ASSUMES you have this node in your package
    # If you don't have this node, comment out or remove this section
    joystick_controller_cmd = Node(
        package='tilt_drone',  # ASSUMES package name is 'tilt_drone'
        executable='tilt_rotor_joystick_controller',  # ASSUMES this executable exists
        name='tilt_rotor_joystick_controller',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(use_joystick),
        output='screen'
    )

    # ============================================================================
    # LAUNCH DESCRIPTION ASSEMBLY
    # ============================================================================
    
    # Create launch description
    ld = LaunchDescription()

    # Add launch arguments
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_gui_cmd)
    ld.add_action(declare_headless_cmd)
    ld.add_action(declare_use_joystick_cmd)
    ld.add_action(declare_use_external_config_cmd)

    # Add nodes with proper timing to ensure proper startup sequence
    
    # Start Gazebo first
    ld.add_action(start_gazebo_cmd)
    ld.add_action(start_gazebo_headless_cmd)
    
    # Start robot description and bridge immediately
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(bridge_cmd)
    
    # Wait for Gazebo to fully start, then spawn robot (5 seconds)
    ld.add_action(TimerAction(
        period=5.0,
        actions=[spawn_robot_cmd]
    ))
    
    # Wait for robot to spawn, then start controller manager (8 seconds)
    ld.add_action(TimerAction(
        period=8.0,
        actions=[controller_manager_cmd]
    ))
    
    # Start joint state broadcaster first (12 seconds)
    ld.add_action(TimerAction(
        period=12.0,
        actions=[joint_state_broadcaster_cmd]
    ))
    
    # Start all tilt controllers (15 seconds)
    ld.add_action(TimerAction(
        period=15.0,
        actions=[
            left_front_tilt_controller_cmd,
            left_rear_tilt_controller_cmd,
            right_front_tilt_controller_cmd,
            right_rear_tilt_controller_cmd
        ]
    ))
    
    # Start all propeller controllers (18 seconds)
    ld.add_action(TimerAction(
        period=18.0,
        actions=[
            left_front_prop_controller_cmd,
            left_rear_prop_controller_cmd,
            right_front_prop_controller_cmd,
            right_rear_prop_controller_cmd
        ]
    ))
    
    # Start joystick control last (20 seconds)
    ld.add_action(TimerAction(
        period=20.0,
        actions=[joystick_cmd, joystick_controller_cmd]
    ))

    return ld
