# -*- coding: utf-8 -*-

import os
import posixpath
try:
    from urllib.parse import SplitResult, urlunsplit
except ImportError:
    from urlparse import SplitResult, urlunsplit

from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_bootstrap import Bootstrap as bootstrap
from flask_security import Security, SQLAlchemyUserDatastore
from flask_uploads import UploadSet, configure_uploads

from . import config
from . import models
from .admin import admin, ModelView
from .nav import nav


# Flask app
app = Flask('slim')
app.config.from_object(config)
app.config.from_object(config)
app.config.update(
    SQLALCHEMY_DATABASE_URI=urlunsplit(SplitResult(
        scheme='sqlite',
        netloc='/',
        path=posixpath.join(app.instance_path, 'slim.db'),
        query='',
        fragment='')),
    UPLOADED_REQUESTS_DEST=os.path.join(app.instance_path, 'uploads'),
)
app.config.from_pyfile(
    app.config['SLIM_SYSTEM_CONFIG_FILE'],
    silent=True if app.config['DEBUG'] or app.config['TESTING'] else False)
app.config.from_envvar('SLIM_SETTINGS_PATH', silent=True)


# bootstrap
bootstrap(app)


# sqlalchemy
db = models.db
db.init_app(app)


# security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


# admin
ModelView.page_size = app.config.get('SLIM_ITEMS_PER_PAGE', 5)
admin.name = app.config.get('SLIM_APPNAME', 'SLiM')
#admin.url = '/'  # url_for('index')
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
request_uploader = UploadSet('requests', app.config['SLIM_REQUEST_EXTENSIONS'])
configure_uploads(app, request_uploader)
