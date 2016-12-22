# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap as bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads
from flask_migrate import Migrate

from . import config


# Flask app
app = Flask('areweblic')
app.config.from_object(config)

# bootstrap
bootstrap(app)

# sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# flask-uploads
request_uploader = UploadSet('requests', app.config['REQUEST_EXTENSIONS'])
configure_uploads(app, request_uploader)
