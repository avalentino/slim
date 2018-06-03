# -*- coding: utf-8 -*-

from __future__ import absolute_import

import posixpath
from functools import partial

from flask import request, current_app
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link, Subgroup
from flask_security import current_user

from . import utils


nav = Nav()


@nav.navigation('top')
def topnavbar():
    # support link
    support_email = current_app.config['SLIM_SUPPORT_EMAIL']
    support_link = utils.make_support_link(support_email)

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
        except Exception:
            # @COMPATIBILITY: Python < 3.5
            del path_views[:]
            # path_views.clear()
            break
        target = rule.endpoint
        path_views.append(View('> ' + label.capitalize(), target))

    # navbar
    app_name = current_app.config.get('SLIM_APPNAME', 'SLiM')
    items = [
        View(app_name, 'index'),
        View('Home', 'index'),
    ]
    if current_user.has_role('admin'):
        items.extend([
            View('Admin', 'admin.index'),
        ])
    items.extend([
        Link('Support', support_link),
        View('About', 'about'),
    ])

    if current_user.is_authenticated:
        subgroup = Subgroup(
            current_user.email,
            View('Profile', 'user_profile'),
            View('Logout', 'security.logout'),
        )

        items.append(subgroup)

    if path_views:
        items[2:2] = path_views

    return Navbar(*items)
