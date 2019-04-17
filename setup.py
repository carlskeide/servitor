# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='Servitor',
    version='1.0.4',

    description='Tiny webhook for pushing images to docker swarm services',
    url='https://github.com/carlskeide/servitor/',
    author='Carl Skeide',

    packages=find_packages(),

    install_requires=[
        "flask",
        "flask-restful",
        "requests",
        "PyYAML",
        "docker"
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'flake8'
        ],
    }
)
