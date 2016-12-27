# -*- coding: utf-8 -*-

import os
import posixpath
from collections import OrderedDict
try:
    from urllib.parse import SplitResult, urlunsplit
except ImportError:
    from urlparse import SplitResult, urlunsplit


# app
DEBUG = True

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
APPLICATION_DIR = os.path.normpath(os.path.join(APPLICATION_DIR, os.pardir))
SYSTEM_CONFIG_FILE = '/etc/areweblic/config.py'
# SERVER_NAME = ''

SECRET_KEY = 'something hard to guess'


# sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = urlunsplit(SplitResult(
    scheme='sqlite',
    netloc='/',
    path=posixpath.join(APPLICATION_DIR, 'arelic.db'),
    query='',
    fragment=''))


# security
SECURITY_CONFIRMABLE = False
SECURITY_TRACKABLE = True
SECURITY_LOGIN_USER_TEMPLATE = 'login.html'


# upload
MAX_CONTENT_LENGTH = 4096

UPLOADED_REQUESTS_DEST = os.path.join(APPLICATION_DIR, 'uploads')
UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'

REQUEST_EXTENSIONS = ('request',)


# areweblic
LICENSE_GENERATOR_PATH = os.path.join(
    APPLICATION_DIR, 'bin', 'generate_license.bin')

# TODO: get this form the DB
PRODUCTS = OrderedDict([
    ('ssp', 'SSP'),
    ('cspp', 'CSPP'),
    ('csip', 'CSIP'),
    ('gss', 'GSS'),
])
