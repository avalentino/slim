#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='areweblic',
    packages=['areweblic'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-bootstrap',
        # 'flask-login',
        'flask-migrate',
        'flask-sqlalchemy',
        'flask-uploads',
        # 'flask-user',
    ],
)
