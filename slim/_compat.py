# -*- coding: utf-8 -*-

"""Compatibility tools for the SLiM Flask application."""

# @COMPATIBILITY: Python < 3.0
try:
    from urllib.parse import ParseResult, urlunparse, urlsplit, quote
except ImportError:
    from urlparse import ParseResult, urlunparse, urlsplit
    from urllib import quote


# @COMPATIBILITY: Flask-Security < 2.0.2
try:
    from flask_security.utils import hash_password
except ImportError:
    from flask_security.utils import encrypt_password as hash_password


__all__ = ['hash_password', 'ParseResult', 'urlunparse', 'urlsplit', 'quote']
