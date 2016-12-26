# -*- coding: utf-8 -*-

import os
import sys
import logging
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from flask_security.utils import encrypt_password

from areweblic.app import app, db, user_datastore


# basic cli initialization
logging.basicConfig(
    format='%(levelname)s: %(message)s', level=logging.INFO, stream=sys.stdout)
log = logging.getLogger('arelweblic.cli')

manager = Manager(app)


# === basic db init ==========================================================
@manager.command
def init_db():
    """Basic initialization of the internal DB"""

    db_path = urlsplit(app.config['SQLALCHEMY_DATABASE_URI']).path
    db_path = os.path.dirname(db_path)
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    db.create_all()

    # roles
    admin_role = user_datastore.create_role(name='admin',
                                            description='Administrator')
    user_datastore.create_role(name='user', description='Standard user')

    # users
    user = user_datastore.create_user(email='admin', password='')
    user_datastore.deactivate_user(user)
    user_datastore.add_role_to_user(user, admin_role)

    log.warning('remember to change the password for admin')

    db.session.commit()


@manager.command
def init_test_db():
    """Basic initialization of the internal DB for testing"""

    init_db()

    # users
    admin = user_datastore.find_user(email='admin')
    admin.password = encrypt_password('admin')

    role = user_datastore.find_role('user')
    for username in ('user1', 'user2'):
        user = user_datastore.create_user(email=username, password=username)
        user_datastore.add_role_to_user(user, role)
        user_datastore.activate_user(user)

    db.session.commit()


# === User management ========================================================
UserManager = Manager(usage='Perform user mamagement')


@UserManager.command
def list():
    """List users"""

    db.create_all()

    from .models import User
    for user in User.query.all():
        print(user)


@UserManager.option('rolename', metavar='role', nargs='?', default='user',
                    help="new user's role (optional)")
@UserManager.option('pwd', help="password for the new user")
@UserManager.option('email', help="new user's email")
def add(email, pwd, rolename='user'):
    """Add a new user"""

    from sqlalchemy.exc import IntegrityError

    db.create_all()

    user = user_datastore.create_user(email=email, password=pwd)

    role = user_datastore.find_role(rolename)
    if not role:
        log.error('role %r does not exist', rolename)
    else:
        try:
            user_datastore.add_role_to_user(user, role)
            user_datastore.activate_user(user)
            db.session.commit()
        except IntegrityError:
            log.error('user %r already exists', user.email)
        else:
            log.info('new %r user correctly added', email)


@UserManager.option('email', help="new user's email")
def remove(email):
    """Remove an existing user"""

    db.create_all()

    user = user_datastore.find_user(email=email)
    if not user:
        log.error('user %r does not exist', email)
    else:
        user_datastore.delete_user(user)

        db.session.commit()
        log.info('user %r removed', email)


@UserManager.option('email', help="new user's email")
def enable(email, enable=True):
    """Enable an existing user"""

    db.create_all()

    user = user_datastore.find_user(email=email)
    if not user:
        log.error('user %r does not exist', email)
    else:
        if enable:
            user_datastore.activate_user(user)
        else:
            user_datastore.deactivate_user(user)

        db.session.commit()
        log.info('user %r %s', email, 'enabled' if enable else 'disabled')


@UserManager.option('email', help="new user's email")
def disable(email):
    """Disable an existing user"""

    return enable(email, False)


@UserManager.option('newpwd', metavar='password', help='new password')
@UserManager.option('email', help="new user's email")
def change_password(email, newpwd):
    """Change the password of an existing user"""

    db.create_all()

    user = user_datastore.find_user(email=email)
    if not user:
        log.error('user %r does not exist', email)
    else:
        user.password = encrypt_password(newpwd)

        db.session.commit()
        log.info('user %r password changed', email)


# === Main ===================================================================
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('user', UserManager)

manager.run()
