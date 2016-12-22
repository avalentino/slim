# -*- coding: utf-8 -*-

import datetime

from .app import db


class License(db.Model):
    __tablename__ = 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), default='user', nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.String(64))
    description = db.Column(db.String(100))
    request = db.Column(db.LargeBinary)
    rewuest_date = db.Column(db.DateTime)
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
