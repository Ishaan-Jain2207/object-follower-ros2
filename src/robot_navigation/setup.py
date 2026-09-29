from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'robot_navigation'

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),
        (
            os.path.join("share", package_name, "config"),
            glob("config/*"),
        ),
        
        (
            os.path.join(
                "share",
                package_name,
                "maps",
                "rooms",
            ),
            [
                "maps/rooms/room_map.pgm",
                "maps/rooms/room_map.yaml",
            ],
        ),
        (
            os.path.join("share", package_name, "rviz"),
            glob("rviz/*"),
        ),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sampath',
    maintainer_email='sampath@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'adafruit_navigation = robot_navigation.adafruit_navigate:main',
        ],
    },
)
