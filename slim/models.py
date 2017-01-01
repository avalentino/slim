# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


# Security
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role: id=%d, name=%r, description=%r>' % (
            self.id, self.name, self.description)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.String(255))
    # last_name = db.Column(db.String(255))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    # password = db.Column(db.PasswordType(255))
    active = db.Column(db.Boolean())
    # confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users'))  # , lazy='dynamic'))

    def __str__(self):
        return self.email

    def __repr__(self):
        roles = ', '.join([role.name for role in self.roles])
        return '<User: id=%d, email=%r, roles=%r, active=%s>' % (
            self.id, self.email, roles, self.active)


# SLiM
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255), default='')
    url = db.Column(db.String(255), default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Product: id=%d, name=%r' % (self.id, self.name)


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)  # @TODO: check
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer(), default=1)
    # purchase_date = db.Column(db.DateTime())
    # expiration_date = db.Column(db.DateTime())
    # active = db.Column(db.Boolean())

    user = db.relationship(
        'User', backref=db.backref('purchases', lazy='dynamic'))
    product = db.relationship(
        'Product', backref=db.backref('purchases', lazy='dynamic'))

    def __str__(self):
        return 'Purchase(id=%d, user=%r, product=%r, quantity=%d)' % (
            self.id, self.user.email, self.product.name, self.quantity)

    def __repr__(self):
        return '<Purchase: id=%d, user_id=%r, product_id=%r, quantity=%d>' % (
            self.id, self.user_id, self.product_id, self.quantity)

    @classmethod
    def count(cls, user_id=None, product_id=None):
        query = cls.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if product_id:
            query = query.filter_by(product_id=product_id)

        return sum(item.quantity for item in query.all())


class License(db.Model):
    __tablename__ = 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    description = db.Column(db.String(255))
    request = db.Column(db.LargeBinary)
    request_date = db.Column(db.DateTime)
    license = db.Column(db.LargeBinary)

    user = db.relationship(
        'User', backref=db.backref('licenses', lazy='dynamic'))
    product = db.relationship(
        'Product', backref=db.backref('licenses', lazy='dynamic'))

    def __init__(self, **kwargs):
        kwargs.setdefault('request_date', datetime.datetime.now())
        super(License, self).__init__(**kwargs)

    def __str__(self):
        return ('License(id=%d, user=%r, product=%r, request_date=%s)' % (
                self.id, self.user.email, self.product.name,
                self.request_date.isoformat()))

    def __repr__(self):
        return ('<License: id=%d, user_id=%r, product_id=%r, '
                'request_date=%s>' % (self.id, self.user_id, self.product_id,
                                      self.request_date.isoformat()))
