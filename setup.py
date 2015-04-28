#!/usr/bin/env python
from setuptools import setup, find_packages
import os

setup(name='cuzak-tools',
    version='0.0.3',
    description='''
    Parser VFK souboru a konverter jejich obsahu do PostGIS databaze
    ''',
    license='BSD',
    url='https://github.com/smolenka/cuzak-tools',
    author='vencax',
    author_email='vencax@centrum.cz',
    packages=find_packages(),
    install_requires=[
        'psycopg2'
    ],
    keywords="GIS VFK cuzak",
    include_package_data=True,
    data_files=[
        ('share/cuzak_tools', ['README.md']),
        ('bin', ['import_vfk.py']),
    ]
)
