# -*- coding: utf-8 -*-

import os


DEBUG = True

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
APPLICATION_DIR = os.path.normpath(os.path.join(APPLICATION_DIR, os.pardir))

# SERVER_NAME = ''

SECRET_KEY = 'something hard to guess'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    'sqlite:///' + os.path.join(APPLICATION_DIR, 'arelic.db'))

MAX_CONTENT_LENGTH = 4096

UPLOADED_REQUESTS_DEST = os.path.join(APPLICATION_DIR, 'uploads')
UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'

REQUEST_EXTENSIONS = ('request',)

LICENSE_GENERATOR_PATH = os.path.join(
    APPLICATION_DIR, 'bin', 'generate_license.bin')
