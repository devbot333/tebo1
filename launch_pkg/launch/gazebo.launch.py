import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    package_name = "launch_pkg"
    world_path = "~/tebo1_dev_ws/src/descriptions_pkg/worlds/obstacles.world"

    state_publisher_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'state_publisher.launch.py'
        )])
    )

    #RUNNING GAZEBO

    #THIS WAY DID NOT WORK
    # gazebo = IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource([os.path.join(
    #             get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #             launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
    #         )

    run_gazebo = ExecuteProcess(
            cmd=['gazebo', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path],
            output='screen'
        )
    
    spawn_entity = Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=[
                '-topic','robot_description',
                '-entity','dana_bot'
                ],
            output='screen'
        )
    

    return LaunchDescription([
        state_publisher_node,
        run_gazebo,
        spawn_entity
    ])
    

