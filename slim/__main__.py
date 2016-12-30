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

from slim.app import app, user_datastore
from slim.models import db, User, License, Product, Purchase


# basic cli initialization
logging.basicConfig(
    format='%(levelname)s: %(message)s', level=logging.INFO, stream=sys.stdout)
log = logging.getLogger('slim.cli')

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


def _init_test_db(products=None):
    init_db()

    # products
    if products is None:
        products = (
            ('product1', 'Product n. 1 description'),
            ('product2', 'Product n. 1 description'),
            ('product3', 'Product n. 1 description'),
        )
    for name, description in products:
        product = Product(name=name, description=description)
        db.session.add(product)

    # users
    admin = user_datastore.find_user(email='admin')
    admin.password = encrypt_password('admin')
    user_datastore.activate_user(admin)

    role = user_datastore.find_role('user')
    for username in ('user1', 'user2'):
        user = user_datastore.create_user(email=username,
                                          password=encrypt_password(username))
        user_datastore.add_role_to_user(user, role)
        user_datastore.activate_user(user)

    # purchases
    for product in Product.query.all():
        purchase = Purchase(
            user_id=admin.id, product_id=product.id, quantity=1024)
        db.session.add(purchase)

    nusers = User.query.count()
    for idx, product in enumerate(Product.query.all()):
        user = User.query.get(idx % (nusers - 1) + 2)  # exclude admin
        purchase = Purchase(user_id=user.id, product_id=product.id)
        db.session.add(purchase)

    # licenses
    for product in Product.query.all():
        license = License(
            user_id=admin.id,
            product_id=product.id,
            request=b'dummy',
            license=b'dummy',
        )
        db.session.add(license)

    nusers = User.query.count()
    for idx, product in enumerate(product.query.all()):
        user = User.query.get(idx % (nusers - 1) + 2)  # exclude admin
        license = License(
            user_id=user.id,
            product_id=product.id,
            request=b'dummy',
            license=b'dummy',
        )
        db.session.add(license)

    db.session.commit()


@manager.command
def init_test_db():
    """Basic initialization of the internal DB for testing"""

    return _init_test_db()


# === User management ========================================================
UserManager = Manager(usage='Perform user management')


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
def enable(email, enabled=True):
    """Enable an existing user"""

    db.create_all()

    user = user_datastore.find_user(email=email)
    if not user:
        log.error('user %r does not exist', email)
    else:
        if enabled:
            user_datastore.activate_user(user)
        else:
            user_datastore.deactivate_user(user)

        db.session.commit()
        log.info('user %r %s', email, 'enabled' if enabled else 'disabled')


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


def main():
    manager.run()


if __name__ == '__main__':
    main()
