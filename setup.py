from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'farm_bot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), 
            glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'urdf'), 
            glob(os.path.join('urdf', '*.xacro'))),
        (os.path.join('share', package_name, 'worlds'), 
            glob(os.path.join('worlds', '*.sdf'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosey',
    maintainer_email='rosey@example.com',
    description='Farm robot with obstacle avoidance',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obstacle_avoidance = farm_bot.obstacle_avoidance:main'
        ],
    },
)