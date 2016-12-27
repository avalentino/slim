# -*- coding: utf-8 -*-

import posixpath
from functools import partial
try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote

from flask import request, current_app
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link
from flask_security import current_user


def make_support_link(email):
    support_link_parts = ParseResult(
        scheme='mailto',
        netloc='',
        path=email,
        params='',
        query='subject=' + quote('[AreWebLic] Support request'),
        # query=urlencode({'subject': '[AreWebLic] Support request'},
        #                 quote_via=quote),
        fragment='',
    )
    return urlunparse(support_link_parts)

nav = Nav()


@nav.navigation('top')
def topnavbar():
    # support link
    support_link = make_support_link(current_app.config['SUPPORT_EMAIL'])

    # navigation path
    server_name = current_app.config['SERVER_NAME']
    server_name = server_name if server_name else 'localhost'
    url_adapter = current_app.url_map.bind(server_name)
    match = partial(url_adapter.match, return_rule=True)

    path_views = []
    path_parts = request.path.strip(posixpath.sep).split(posixpath.sep)
    for idx, item in enumerate(path_parts[:-1], start=1):
        label = item.strip(posixpath.sep)
        path = posixpath.join('/', *path_parts[:idx])
        try:
            rule, _ = match(path)
        except Exception:  # RequestRedirect, NotFound
            path_views.clear()
            break
        target = rule.endpoint
        path_views.append(View(label.capitalize(), target))

    # navbar
    if current_user.has_role('admin'):
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            #View('Admin', 'admin_index'),
            Link('Support', support_link),
            View('Logout %s' % current_user.email, 'security.logout'),
        ]
    else:
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            Link('Support', support_link),
        ]
        if current_user.is_authenticated:
            items.append(
                View('Logout %s' % current_user.email, 'security.logout')
            )

    if path_views:
        items[2:2] = path_views

    return Navbar(*items)
