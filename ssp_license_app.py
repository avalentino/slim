#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime

from flask import (
    Flask, request, redirect, url_for, flash, render_template, make_response)
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, UploadNotAllowed
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager, login_required


# ### config.py ##############################################################
# DEBUG = True

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

MAX_CONTENT_LENGTH = 4096

UPLOADED_REQUESTS_DEST = os.path.join(APPLICATION_DIR, 'uploads')
UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'

SECRET_KEY = 'something hard to guess'

SQLALCHEMY_DATABASE_URI = (
    'sqlite:///' + os.path.join(APPLICATION_DIR, 'ssplic.db'))


# ### app.py #################################################################
app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

REQUEST_EXTENSIONS = ('request',)
license_requests = UploadSet('requests', REQUEST_EXTENSIONS)
configure_uploads(app, license_requests)

db = SQLAlchemy(app)


# ### models.py ##############################################################
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


# ### views.py ###############################################################
@app.route('/')
def index():
    return render_template('index.html', count=LicenseRequest.query.count())


@app.route('/uploaded')
def uploaded():
    return render_template('uploaded.html', items=LicenseRequest.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST' and 'license_req' in request.files:
        try:
            filename = license_requests.save(request.files['license_req'])
        except UploadNotAllowed as ex:
            flash('Upload not allowed: incorrect file type', 'error')
        else:
            flash('Request file saved to %r.' % filename)

            filename = os.path.join(UPLOADED_REQUESTS_DEST, filename)
            with open(filename, 'rb') as fd:
                data = fd.read()

            req = LicenseRequest(
                'user_id',
                product=request.form['product'],
                request=data,
                description=request.form['description'])

            db.session.add(req)
            db.session.commit()

            os.remove(filename)

            return redirect(url_for('uploaded'))
    return render_template('new.html')


@app.route('/request/<int:req_id>')
def show_request(req_id):
    req = LicenseRequest.query.get(req_id)
    return render_template('request.html', req=req)


@app.route('/download/<int:req_id>')
def download(req_id):
    req = LicenseRequest.query.get(req_id)
    #data = req.license     # XXX
    data = req.request

    response = make_response(data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=lic.dat'

    return response

## http://www.patricksoftwareblog.com/tag/flask-uploads/

#~ login_manager = LoginManager()
#~ login_manager.init_app(app)
#~ login_manager.login_view = "users.login"



############################################################
#~ from flask_wtf import Form
#~ from wtforms import StringField
#~ from wtforms.validators import DataRequired
#~ from flask_wtf.file import FileField, FileAllowed, FileRequired


#~ class LicenseRequestForm(Form):
    #~ username = StringField('User', validators=[DataRequired()])
    #~ description = StringField('Description', validators=[DataRequired()])
    #~ license_request = FileField(
        #~ 'License request file',
        #~ validators=[FileRequired(),
                    #~ FileAllowed(license_requests, 'request file (*.request)')])


############################################################

#~ def flash_errors(form):
    #~ for field, errors in form.errors.items():
        #~ for error in errors:
            #~ flash(u"Error in the %s field - %s" % (
                #~ getattr(form, field).label.text,
                #~ error
            #~ ))

#~ @app.route('/new', methods=['GET', 'POST'])
#~ #@login_required
#~ def new_request():
    #~ form = LicenseRequestForm()
    #~ if request.method == 'POST':
        #~ if form.validate_on_submit():
            #~ now = datetime.datetime.now()
            #~ filename = license_requests.save(
                #~ request.files['license_request'],
                #~ folder=now.strftime('%Y%m%d-%H-%M-%S.%f'))
            #~ url = license_requests.url(filename)
            #~ # save to db
            #~ #with open(url, 'rb') as fd:
            #~ #    req = fd.read()
            #~ #db.session.add(req)
            #~ #db.session.commit()
            #~ flash('New request, saved!', 'success')
            #~ return redirect(url_for('recipes.user_recipes'))
        #~ else:
            #~ flash_errors(form)
            #~ flash('ERROR! Request was not added.', 'error')

    #~ return render_template('requestform.html', form=form)


def init_db():
    db.create_all()

    req = LicenseRequest('user_id', 'SSP', '', 'descr')

    db.session.add(req)
    db.session.commit()


if __name__ == "__main__":
    # env FLASK_APP=ssp_license_app.py FLASK_DEBUG=1 python -m flask run
    app.run()
