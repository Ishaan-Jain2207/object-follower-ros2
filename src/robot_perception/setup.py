from setuptools import setup
from glob import glob

package_name = 'robot_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='newans',
    maintainer_email='sampathguggilapu@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'detect_ball = robot_perception.detect_ball:main',
            'detect_ball_3d = robot_perception.detect_ball_3d:main',
            'follow_ball = robot_perception.follow_ball:main',
            'shapes_tracker = robot_perception.shapes_tracker:main',
            'owner_follower = robot_perception.owner_follower:main',
        ],
    },
)
