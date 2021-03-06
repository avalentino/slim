#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for the SLiM Flask application."""

import os
import re
import sys
from setuptools import setup


PROJECT = 'slim'


def get_version(filename=None):
    """Return the version string read form the specified file."""

    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), PROJECT, '__init__.py')

    with open(filename) as fd:
        src = fd.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", src, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


def compat_requites():
    """Return the list of additional requirements for old Python versions."""

    reqlist = []

    if sys.version_info < (3, 3, 0):
        reqlist.append('mock')

    if sys.version_info < (2, 7, 0):
        reqlist.append('future')

    return reqlist


setup(
    name=PROJECT,
    version=get_version(),
    description='A Simple License Management system',
    author='Antonio Valentino',
    author_email='antonio.valentino@tiscali.it',
    license='MIT',
    packages=['slim'],
    include_package_data=True,
    package_data={
        'slim': [
            'templates',
        ],
    },
    entry_points={
        'console_scripts': [
            'slimcli = slim.__main__:main',
        ],
    },
    url='https://github.com/avalentino/slim',
    install_requires=[
        'Flask',
        'Flask-Admin',
        'Flask-Bootstrap',
        'Flask-Migrate',
        'flask-nav',
        'Flask-Script',
        'Flask-Security',
        'Flask-SQLAlchemy',
        'Flask-Testing',
        'Flask-Uploads',
        'Flask-WTF',
        'Jinja2',
        # 'future',     # Python < 2.7
        # 'mock',       # Python < 3.3
        'setuptools'
    ] + compat_requites(),
    test_suite='tests',
)
