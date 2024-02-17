from setuptools import setup, find_packages

setup(
    name='create-ros-project',
    version='0.1',
    description='Create a ROS project and manage system dependencies with one command.',
    url='',
    author='Jingxiang Mo',
    author_email='jingxiangmo@gmail.com',
    license='',
    install_requires=['questionary', 'toml'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['rq=src.main:script']
    )
)