# -*- coding: utf-8 -*-

try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote


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


def expand_cmd_vars(cmdargs, **kwargs):
    return [item % kwargs for item in cmdargs]
