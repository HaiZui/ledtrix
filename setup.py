'''
ledtrix package setup
'''
import os
from setuptools import setup, find_packages

setup(
    name="ledtrix",
    version="0.0.0",
    author="Teemu Parviainen",
    author_email="parviainen.teemu@gmail.com",
    description=("Led strip/matrix effect library"),
    license="Teemu Parviainen",
    keywords="led",
    url="https://github.com/HaiZui/raspberry-leds",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame'
    ],
    classifiers=[],
)