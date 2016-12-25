# -*- coding: utf-8 -*-

try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote

from flask import Flask
from flask_bootstrap import Bootstrap as bootstrap
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_uploads import UploadSet, configure_uploads
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link

from . import config
from . import models


# Flask app
app = Flask('areweblic')
app.config.from_object(config)


# bootstrap
bootstrap(app)


# nav
nav = Nav()


@nav.navigation('top')
def topnavbar():
    parts = ParseResult(
        scheme='mailto',
        netloc='',
        path='info@aresys.it',
        params='',
        query='subject=' + quote('[AreWebLic] Support request'),
        # query=urlencode({'subject': '[AreWebLic] Support request'},
        #                 quote_via=quote),
        fragment='',
    )
    support_link = urlunparse(parts)

    return Navbar(
        View('AreWebLic', 'index'),
        View('Home', 'index'),
        Link('Support', support_link),
        View('Logout %s' % current_user.email, 'security.logout'),
    )


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
