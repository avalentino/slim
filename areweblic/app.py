# -*- coding: utf-8 -*-

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
request_uploader = UploadSet('requests', app.config['REQUEST_EXTENSIONS'])
configure_uploads(app, request_uploader)
