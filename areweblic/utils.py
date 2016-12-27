# -*- coding: utf-8 -*-

try:
    from urllib.parse import ParseResult, urlunparse, quote
except ImportError:
    from urlparse import ParseResult, urlunparse
    from urllib import quote


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
