# -*- coding: utf-8 -*-

import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


# Secutiry
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role(id=%d, name=%r, description=%r)>' % (
            self.id, self.name, self.description)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    #first_name = db.Column(db.String(255))
    #last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    #confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        roles = ', '.join([role.name for role in self.roles])
        return '<User(id=%d, email=%r, roles=%r, active=%s)>' % (
            self.id, self.email, roles, self.active)


# areweblic
class License(db.Model):
    __tablename__ = 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.Column(db.String(64))
    description = db.Column(db.String(100))
    request = db.Column(db.LargeBinary)
    request_date = db.Column(db.DateTime)
    license = db.Column(db.LargeBinary)

    def __init__(self, user_id, product, request, license, description='',
                 request_date=None):

        if request_date is None:
            request_date = datetime.datetime.now()

        self.user_id = user_id
        self.product = product
        self.description = description
        self.request = request
        self.request_date = request_date
        self.license = license

    def __repr__(self):
        return '<License: id=%d, user_id=%r, product=%r, request_date=%s>' % (
            self.id, self.user_id, self.product, self.date.isoformat())
