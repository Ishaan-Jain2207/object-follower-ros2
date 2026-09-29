import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():


    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robot_description"),
            "launch",
            "balltrack_gazebo.launch.py",
        ),
    )

    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("robot_controller"),
                "launch",
                "controller.launch.py",
            )
        ),
    )

    teleop = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robot_controller"),
            "launch",
            "teleop.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "True"
        }.items()
    )

    rviz_config = os.path.join(
        get_package_share_directory("robot_description"),
        "rviz",
        "display.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[{
            "use_sim_time": True
        }]
    )

    return LaunchDescription(
        [
            gazebo,
            controller,
            teleop,
            rviz_node,
        ]
    )