from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    robot_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robot_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    start_robot_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster,
            on_exit=[robot_controller],
        )
    )

    return LaunchDescription([
        joint_state_broadcaster,
        start_robot_controller,
    ])
