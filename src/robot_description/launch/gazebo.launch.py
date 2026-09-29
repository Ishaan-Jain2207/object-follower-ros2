import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    robot_description_pkg = get_package_share_directory(
        "robot_description"
    )

    # Robot model argument
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            robot_description_pkg,
            "urdf",
            "robot.urdf.xacro",
        ),
        description="Absolute path to robot URDF/Xacro file",
    )

    # Gazebo world argument
    world_name_arg = DeclareLaunchArgument(
        name="world_name",
        default_value="rooms",
        description="Name of the Gazebo world",
    )

    # Gazebo world path
    world_path = PathJoinSubstitution(
        [
            robot_description_pkg,
            "worlds",
            PythonExpression(
                [
                    "'",
                    LaunchConfiguration("world_name"),
                    "'",
                    " + '.world'",
                ]
            ),
        ]
    )

    # Robot description generated from Xacro
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                LaunchConfiguration("model"),
            ]
        ),
        value_type=str,
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
        output="screen",
    )

    # Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": PythonExpression(
                [
                    "'",
                    world_path,
                    " -v 4 -r'",
                ]
            )
        }.items(),
    )

    # Spawn robot into Gazebo
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "2wheeled_robot",
        ],
    )

    # ROS 2 <-> Gazebo Bridge
    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": os.path.join(
                    robot_description_pkg,
                    "config",
                    "gz_bridge.yaml",
                )
            }
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            model_arg,
            world_name_arg,
            robot_state_publisher_node,
            gazebo,
            gz_spawn_entity,
            gz_ros2_bridge,
        ]
    )