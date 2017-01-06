# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

from . import utils


# --- slim -------------------------------------------------------------------
SLIM_APPNAME = 'SLiM'
SLIM_WELCOME_MESSAGE = 'Simple License Management system (SLiM)'
SLIM_COPYRIGHT_YEAR = 2017
SLIM_COPYRIGHT_URL = 'http://slimapp.org'
SLIM_COPYRIGHT_OWNER = 'Antonio Valentino'
SLIM_SUPPORT_EMAIL = 'support@slimapp.org'
SLIM_INSTANCE_CONFIG_FILE = 'config.py'
SLIM_SYSTEM_CONFIG_FILE = '/etc/slim/config.py'
SLIM_ITEMS_PER_PAGE = 5
SLIM_REQUEST_EXTENSIONS = ('request',)
SLIM_LICENSE_GENERATOR_CMD = [
    sys.executable,
    '-u',
    os.path.join(utils.package_prefix(), 'bin', 'dummy-generate-license.py'),
    '%(INPUT_REQUEST_FILE)s',
    '%(OUTPUT_LICENSE_FILE)s',
]
# SLIM_PLUGIN = None
SLIM_FILE_LOGGING_LEVEL = None   # no logging on file
SLIM_FILE_LOGGING_FORMAT = (
    '%(asctime)s - %(name)s - %(levelname)s: %(message)s')
SLIM_FILE_LOGGING_MAXBYTES = 10 * 1024**2   # 10 MB
SLIM_FILE_LOGGING_BACKUPCOUNT = 5


# --- flask ------------------------------------------------------------------
# DEBUG = True
# TESTING = False
SECRET_KEY = 'something hard to guess'      # XXX: change this
# SERVER_NAME = 'slim.local'
MAX_CONTENT_LENGTH = 4 * 1024


# --- bootstrap --------------------------------------------------------------
# BOOTSTRAP_SERVE_LOCAL = False


# --- sqlalchemy -------------------------------------------------------------
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'


# --- security ---------------------------------------------------------------
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'slimsalt'         # XXX: change this
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE = False
SECURITY_TRACKABLE = True
SECURITY_PASSWORDLESS = False
SECURITY_CHANGEABLE = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False


# --- upload -----------------------------------------------------------------
UPLOADED_REQUESTS_DEST = os.path.join('instance', 'uploads')
# UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'
