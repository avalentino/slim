# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_bootstrap import Bootstrap
from flask_security import Security, SQLAlchemyUserDatastore
from flask_uploads import UploadSet, configure_uploads

from . import config
from . import models
from . import utils
from .admin import admin, ModelView
from .nav import nav


# Flask app setup
def logging_config(app):
    level = app.config['SLIM_FILE_LOGGING_LEVEL']
    if level is None:
        return

    werkzeug_logger = logging.getLogger('werkzeug')
    level = logging.getLevelName(level)

    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    formatter = logging.Formatter(app.config['SLIM_FILE_LOGGING_FORMAT'])

    handler = logging.handlers.RotatingFileHandler(
        os.path.join(app.instance_path, 'slim.log'),
        maxBytes=app.config['SLIM_FILE_LOGGING_MAXBYTES'],
        backupCount=app.config['SLIM_FILE_LOGGING_BACKUPCOUNT'])
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    app.logger.addHandler(handler)
    logging.getLogger('werkzeug').addHandler(handler)

    # set log level
    app.logger.setLevel(level)
    werkzeug_logger.setLevel(level)
    app.logger.info(
        'log level set to %r', app.config['SLIM_FILE_LOGGING_LEVEL'])


def default_app_config(app):
    app.config.update(
        SQLALCHEMY_DATABASE_URI=utils.sqlite_uri_for(
            os.path.join(app.instance_path, 'slim.db')),
        SLIM_LOGGING_FILENAME=os.path.join(app.instance_path, 'slim.log'),
        UPLOADED_REQUESTS_DEST=os.path.join(app.instance_path, 'uploads'),
    )
    app.config.from_pyfile(app.config['SLIM_INSTANCE_CONFIG_FILE'], silent=True)
    app.config.from_pyfile(app.config['SLIM_SYSTEM_CONFIG_FILE'], silent=True)
    app.config.from_envvar('SLIM_SETTINGS_PATH', silent=True)

    logging_config(app)


def setup_components(app):
    # bootstrap
    Bootstrap(app)

    # sqlalchemy
    models.db.init_app(app)

    # security
    user_datastore = SQLAlchemyUserDatastore(models.db, models.User,
                                             models.Role)
    security = Security(app, user_datastore)

    # admin
    ModelView.page_size = app.config.get('SLIM_ITEMS_PER_PAGE', 5)
    admin.name = app.config.get('SLIM_APPNAME', 'SLiM')
    admin.init_app(app)

    # define a context processor for merging flask-admin's template context
    # into the flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # nav
    nav.init_app(app)

    # flask-uploads
    # patch_request_class(app, app.config['MAX_CONTENT_LENGTH'])
    request_uploader = UploadSet('requests',
                                 app.config['SLIM_REQUEST_EXTENSIONS'])
    configure_uploads(app, request_uploader)

    # components
    components = dict(
        user_datastore=user_datastore,
        security=security,
        request_uploader=request_uploader,
    )

    return components


def create_app(app=None, cfg=None):
    if app is None:
        app = Flask('slim', instance_relative_config=True)
        app.config.from_object(config)

    default_app_config(app)

    if cfg:
        app.comfig.from_mapping(**cfg)

    components = setup_components(app)

    return app, components


app, components = create_app()
