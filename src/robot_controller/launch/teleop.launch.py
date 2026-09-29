import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    robot_controller_pkg = get_package_share_directory(
        "robot_controller"
    )

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
        description="Use simulated time",
    )

    twist_mux_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("twist_mux"),
                "launch",
                "twist_mux_launch.py",
            )
        ),
        launch_arguments={
            "cmd_vel_out": "robot_controller/cmd_vel_unstamped",
            "config_locks": os.path.join(
                robot_controller_pkg,
                "config",
                "twist_mux_locks.yaml",
            ),
            "config_topics": os.path.join(
                robot_controller_pkg,
                "config",
                "twist_mux_topics.yaml",
            ),
            "use_sim_time": LaunchConfiguration("use_sim_time"),
        }.items(),
    )

    twist_relay_node = Node(
        package="robot_controller",
        executable="twist_relay",
        name="twist_relay",
        parameters=[
            {
                "use_sim_time": LaunchConfiguration("use_sim_time"),
            }
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            twist_mux_launch,
            twist_relay_node,
        ]
    )