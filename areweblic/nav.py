# -*- coding: utf-8 -*-

try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote

from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link
from flask_security import current_user

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

    if current_user.has_role('admin'):
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            View('Admin', 'admin_index'),
            Link('Support', support_link),
            View('Logout %s' % current_user.email, 'security.logout'),
        ]
    else:
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            Link('Support', support_link),
            View('Logout %s' % current_user.email, 'security.logout'),
        ]

    return Navbar(*items)

