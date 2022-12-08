import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('mobro_description')
    rviz_config = os.path.join(bringup_dir, 'config', 'default.rviz')

    xacro_path = os.path.join( get_package_share_directory('mobro_description'), 'xacro')
    robot_description = {'robot_description' : Command(['xacro', ' ', xacro_path, '/', 'robot_core', '.urdf.xacro '])}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        arguments=[{'use_sim_time': 'true'}],
        parameters=[robot_description,])

    
    rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', rviz_config],
        parameters=[robot_description,])

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )
    
    # # gazebo2
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
             )
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description', '-entity', 'mobile_robot'],
                        output='screen'
                    )

    # Create the launch description and populate
    ld = LaunchDescription()

    return LaunchDescription([
        # static_tf, 
        rviz_cmd, 
        robot_state_publisher, 
        joint_state_publisher, 
        gazebo, 
        spawn_entity])
    