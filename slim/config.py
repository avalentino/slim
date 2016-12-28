# -*- coding: utf-8 -*-

import os
import posixpath
try:
    from urllib.parse import SplitResult, urlunsplit
except ImportError:
    from urlparse import SplitResult, urlunsplit


# slim
SLIM_APPDIR = os.path.dirname(os.path.realpath(__file__))
SLIM_APPDIR = os.path.normpath(os.path.join(SLIM_APPDIR, os.pardir))
SLIM_APPNAME = 'SLiM'
SLIM_WELCOME_MESSAGE = 'Simple License Management system (SLiM)'
SLIM_COPYRIGHT_YEAR = 2016
SLIM_COPYRIGHT_URL = 'http://slimapp.org'
SLIM_COPYRIGHT_OWNER = 'Antonio Valentino'
SLIM_SUPPORT_EMAIL = 'support@slimapp.org'
SLIM_SYSTEM_CONFIG_FILE = '/etc/slim/config.py'
SLIM_ITEMS_PER_PAGE = 5
SLIM_REQUEST_EXTENSIONS = ('request',)
SLIM_LICENSE_GENERATOR_PATH = os.path.join(
    SLIM_APPDIR, 'bin', 'generate_license.bin')


# app
DEBUG = True
SECRET_KEY = 'something hard to guess'      # @TODO: change this
# SERVER_NAME = 'slim.local'
MAX_CONTENT_LENGTH = 4 * 1024


# sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = urlunsplit(SplitResult(
    scheme='sqlite',
    netloc='/',
    path=posixpath.join(SLIM_APPDIR, 'slim.db'),
    query='',
    fragment=''))


# security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'slimsalt'         # @TODO: change this
SECURITY_CONFIRMABLE = False
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False


# upload
UPLOADED_REQUESTS_DEST = os.path.join(SLIM_APPDIR, 'uploads')
# UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'
