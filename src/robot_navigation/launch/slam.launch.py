import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    slam_config = LaunchConfiguration("slam_config")

    lifecycle_nodes = [
        "slam_toolbox",
        "map_saver_server",
    ]

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true"
    )

    slam_config_arg = DeclareLaunchArgument(
        "slam_config",
        default_value=os.path.join(
            get_package_share_directory("robot_navigation"),
            "config",
            "slam_toolbox.yaml"
        ),
        description="Full path to the SLAM Toolbox configuration file"
    )

    map_saver_server = Node(
        package="nav2_map_server",
        executable="map_saver_server",
        name="map_saver_server",
        output="screen",
        parameters=[
            {
                "save_map_timeout": 5.0,
                "free_thresh_default": 0.196,
                "occupied_thresh_default": 0.65,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="sync_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[
            slam_config,
            {
                "use_sim_time": use_sim_time,
            },
        ],
    )

    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_slam",
        output="screen",
        parameters=[
            {
                "node_names": lifecycle_nodes,
                "autostart": True,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    return LaunchDescription([
        use_sim_time_arg,
        slam_config_arg,
        map_saver_server,
        slam_toolbox,
        lifecycle_manager,
    ])