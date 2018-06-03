# -*- coding: utf-8 -*-

"""Utility functions for the SLiM Flask application."""

from __future__ import absolute_import

import os
import sys

import pkg_resources

from ._compat import ParseResult, urlunparse, quote


__all__ = ['component_version_info']


def package_dir():
    return os.path.dirname(os.path.realpath(__file__))


def package_prefix():
    return os.path.normpath(os.path.join(package_dir(), os.pardir))


def is_installed(instance_path):
    return not instance_path.startswith(package_prefix())


def make_support_link(email, appname='SLiM'):
    support_link_parts = ParseResult(
        scheme='mailto',
        netloc='',
        path=email,
        params='',
        query='subject=' + quote('[%s] Support request' % appname),
        # query=urlencode({'subject': '[%s] Support request' % appname},
        #                 quote_via=quote),
        fragment='',
    )
    return urlunparse(support_link_parts)


def sqlite_uri_for(path):
    uri_parts = ParseResult(
        scheme='sqlite',
        netloc='/',
        path=path,
        params='',
        query='',
        fragment='')

    return urlunparse(uri_parts)


def expand_cmd_vars(cmdargs, **kwargs):
    return [item % kwargs for item in cmdargs]


def to_int(s, default=None):
    """Convert and arbitrary input to `int`.

    Try to convert and arbitrary input to `int` and use a fallback value
    (`default`) if it is not possible.

    """

    try:
        return int(s)
    except (ValueError, TypeError):
        return default


def component_version_info():
    """Return version info of all used Flask components."""

    data = dict(
        flask=dict(
            name='Flask',
            version='',
            url='http://flask.pocoo.org',
        ),
        flask_admin=dict(
            name='Flask Admin',
            version='',
            url='https://github.com/flask-admin/flask-admin',
        ),
        flask_bootstrap=dict(
            name='Flask Bootstrap',
            version='',
            url='http://github.com/mbr/flask-bootstrap',
        ),
        flask_login=dict(
            name='Flask Login',
            version='',
            url='https://github.com/maxcountryman/flask-login',
        ),
        flask_migrate=dict(
            name='Flask Migrate',
            version='',
            url='http://github.com/miguelgrinberg/flask-migrate',
        ),
        flask_nav=dict(
            name='Flask Nav',
            version='',
            url='http://github.com/mbr/flask-nav',
        ),
        flask_principal=dict(
            name='Flask Principal',
            version='',
            url='http://packages.python.org/Flask-Principal',
        ),
        flask_script=dict(
            name='Flask Script',
            version='',
            url='https://github.com/smurfix/flask-script',
        ),
        flask_security=dict(
            name='Flask Security',
            version='',
            url='https://github.com/mattupstate/flask-security',
        ),
        flask_sqlalchemy=dict(
            name='Flask SQLAlchemy',
            version='',
            url='http://github.com/mitsuhiko/flask-sqlalchemy',
        ),
        flask_testing=dict(
            name='Flask Testing',
            version='',
            url='https://github.com/jarus/flask-testing',
        ),
        flask_uploads=dict(
            name='Flask Uploads',
            version='',
            url='https://github.com/maxcountryman/flask-uploads',
        ),
        flask_wtf=dict(
            name='Flask WTF',
            version='',
            url='https://github.com/lepture/flask-wtf',
        ),
        click=dict(
            name='click',
            version='',
            url='http://github.com/mitsuhiko/click',
        ),
        jinja2=dict(
            name='Jinja2',
            version='',
            url='http://jinja.pocoo.org',
        ),
        mock=dict(
            name='Mock',
            version='',
            url='https://github.com/testing-cabal/mock',
        ),
        passlib=dict(
            name='Passlib',
            version='',
            url='https://bitbucket.org/ecollins/passlib',
        ),
        sqlalchemy=dict(
            name='SQLAlchemy',
            version='',
            url='http://www.sqlalchemy.org',
        ),
        werkzeug=dict(
            name='Werkzeug',
            version='',
            url='http://werkzeug.pocoo.org',
        ),
        wtforms=dict(
            name='WTForms',
            version='',
            url='http://wtforms.readthedocs.io/en/latest',
        ),
    )

    for name, info in data.items():
        try:
            module = sys.modules[name]
            info['version'] = module.__version__
        except (KeyError, AttributeError):
            try:
                distribution = pkg_resources.get_distribution(name)
                info['version'] = distribution.version
            except Exception:
                info['version'] = 'N/A'

    return data
