# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote


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
    try:
        return int(s)
    except (ValueError, TypeError):
        return default
