# -*- coding: utf-8 -*-

import datetime

from .app import db


class LicenseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), default='user', nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.String(64))
    description = db.Column(db.String(100))
    request = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime)

    def __init__(self, user_id, product, request, description='', date=None):
        self.user_id = user_id
        self.product = product
        self.description = description
        self.request = request

        if date is None:
            date = datetime.datetime.now()

        self.date = date

    def __repr__(self):
        return ('<LicenseRequest: id=%d, user_id=%r, product=%r, '
                'request_date=%s>' % (self.id, self.user_id, self.product,
                                      self.date.isoformat()))
