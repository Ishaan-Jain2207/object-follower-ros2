from setuptools import find_packages, setup
from glob import glob
import os

package_name = "robot_description"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        # Register package with ament index
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),

        # Install package.xml
        (
            "share/" + package_name,
            ["package.xml"],
        ),

        # Install launch files
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),

        # Install configuration files
        (
            os.path.join("share", package_name, "config"),
            glob("config/*"),
        ),

        # Install URDF / Xacro files
        (
            os.path.join("share", package_name, "urdf"),
            glob("urdf/*"),
        ),

        # Install RViz configuration
        (
            os.path.join("share", package_name, "rviz"),
            glob("rviz/*"),
        ),

        # Install Gazebo worlds
        (
            os.path.join("share", package_name, "worlds"),
            glob("worlds/*"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Your Name",
    maintainer_email="your_email@example.com",
    description="Robot Description package",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        'console_scripts': [
            'publisher_node = robot_description.publisher:main',
            'subscriber_node = robot_description.subscriber:main',
            'demo_node = robot_description.demo_node:main'
        ],
    },
)