# -*- coding: utf-8 -*-

__all__ = ['hash_password']


# @COMPATIBILITY: Flask-Security < 2.0.2
try:
    from flask_security.utils import hash_password
except ImportError:
    from flask_security.utils import encrypt_password as hash_password
