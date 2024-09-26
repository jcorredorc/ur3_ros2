import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Obtener la ruta del paquete y el archivo Xacro
    package_name = 'vacuum_gripper_description'
    xacro_file = 'urdf/vacuum_gripper.xacro'
    
    # Define los argumentos (parámetros) que quieres pasar
    gripper_only_arg = DeclareLaunchArgument(
        'gripper_only',
        default_value='true',  # Valor por defecto
        description='Whether to visualize the gripper without the arm'
    )

    # Generar la ruta completa del archivo Xacro
    xacro_file_path = os.path.join(get_package_share_directory(package_name), xacro_file)

    # Nodo que convertirá el archivo Xacro en URDF y lo publicará en /robot_description
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command([
                'xacro ', xacro_file_path,
                ' gripper_only:=', LaunchConfiguration('gripper_only')  # Pasar el parámetro
            ])
        }]
    )

    # Nodo para lanzar RViz y cargar la configuración
    rviz_config_file = os.path.join(get_package_share_directory(package_name), 'rviz', 'config.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        # Declarar el argumento del parámetro
        gripper_only_arg,
        # Publicar la descripción del robot y lanzar RViz
        robot_state_publisher_node,
        rviz_node
    ])