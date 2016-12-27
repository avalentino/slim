# -*- coding: utf-8 -*-

import os
import posixpath
try:
    from urllib.parse import SplitResult, urlunsplit
except ImportError:
    from urlparse import SplitResult, urlunsplit

from flask import Flask
from flask_bootstrap import Bootstrap as bootstrap
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_uploads import UploadSet, configure_uploads

from . import config
from . import models
from .nav import nav


# Flask app
app = Flask('areweblic')
app.config.from_object(config)
app.config.from_object(config)
app.config.update(
    SQLALCHEMY_DATABASE_URI=urlunsplit(SplitResult(
        scheme='sqlite',
        netloc='/',
        path=posixpath.join(app.instance_path, 'arelic.db'),
        query='',
        fragment='')),
    UPLOADED_REQUESTS_DEST=os.path.join(app.instance_path, 'uploads'),
)
app.config.from_pyfile(
    app.config['SYSTEM_CONFIG_FILE'],
    silent=True if app.config['DEBUG'] or app.config['TESTING'] else False)
app.config.from_envvar('AREWEBLIC_SETTINGS_PATH', silent=True)


# bootstrap
bootstrap(app)


# nav
nav.init_app(app)


# sqlalchemy
db = models.db
db.init_app(app)


# security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


# flask-uploads
#patch_request_class(app, app.config['MAX_CONTENT_LENGTH'])
request_uploader = UploadSet('requests', app.config['REQUEST_EXTENSIONS'])
configure_uploads(app, request_uploader)
