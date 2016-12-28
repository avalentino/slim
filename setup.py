#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='areweblic',
    packages=['areweblic'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_admin',
        'flask-bootstrap',
        'flask-migrate',
        'flask-nav',
        'flask-script',
        'flask-security',
        'flask-sqlalchemy',
        'flask-uploads',
    ],
)
