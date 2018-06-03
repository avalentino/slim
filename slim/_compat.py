# -*- coding: utf-8 -*-

# @COMPATIBILITY: Flask-Security < 2.0.2
try:
    from flask_security.utils import hash_password
except ImportError:
    from flask_security.utils import encrypt_password as hash_password
