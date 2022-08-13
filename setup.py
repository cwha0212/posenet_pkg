from setuptools import setup

package_name = 'posenet_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_publish_node = posenet_pkg.image_publish:main',
            'Posenet_pytorch_node = posenet_pkg.Posenet_pytorch_node:main',
            'train_data_publish_node = posenet_pkg.train_data_publish:main',
            'train_data_rviz_node = posenet_pkg.train_data_rviz:main',
        ],
    },
)
