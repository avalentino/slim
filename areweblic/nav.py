# -*- coding: utf-8 -*-

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
    support_link = utils.make_support_link(current_app.config['SUPPORT_EMAIL'])

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
        path_views.append(View('> ' + label.capitalize(), target))

    # navbar
    if current_user.has_role('admin'):
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            #View('Admin', 'admin_index'),
            Link('Support', support_link),
        ]
    else:
        items = [
            View('AreWebLic', 'index'),
            View('Home', 'index'),
            Link('Support', support_link),
        ]
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
