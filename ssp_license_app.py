#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import datetime
import posixpath

from flask import Flask, request, redirect, url_for, flash, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.uploads import UploadSet, configure_uploads, UploadNotAllowed
#from flask.ext.login import LoginManager, login_required
#from flask_sqlalchemy import SQLAlchemy


UPLOADED_REQUESTS_DEST = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'uploads')
UPLOADED_REQUESTS_URL = 'http://localhost:5001/uploads'

MAX_CONTENT_LENGTH = 4096
SECRET_KEY = 'something hard to guess'

UPLOADED_REQUEST_PATTERN = os.path.join(UPLOADED_REQUESTS_DEST,
                                        '*', '*.request')


app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

REQUEST_EXTENSIONS = ('request',)
license_requests = UploadSet('requests', REQUEST_EXTENSIONS)
configure_uploads(app, license_requests)


@app.route('/')
def index():
    requests = glob.glob(UPLOADED_REQUEST_PATTERN)
    count = len(requests)
    return render_template('index.html', count=count)


@app.route('/uploaded')
def uploaded():
    items = []
    for name in glob.glob(UPLOADED_REQUEST_PATTERN):
        name = os.path.relpath(name, UPLOADED_REQUESTS_DEST)
        items.append((posixpath.join(UPLOADED_REQUESTS_URL, name), name))
    return render_template('uploaded.html', items=items)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST' and 'license_req' in request.files:
        folder = datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.%f')

        try:
            filename = license_requests.save(request.files['license_req'],
                                             folder=folder)
        except UploadNotAllowed as ex:
            flash('Upload not allowed: incorrect file type', 'error')
        else:
            flash('Request file saved to %r.' % filename)
            return redirect(url_for('uploaded'))
    return render_template('new.html')


## http://www.patricksoftwareblog.com/tag/flask-uploads/
#~ db = SQLAlchemy(app)
#~ bcrypt = Bcrypt(app)
#~ mail = Mail(app)

#~ login_manager = LoginManager()
#~ login_manager.init_app(app)
#~ login_manager.login_view = "users.login"

#UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/static/requests/'
#UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/requests/'



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

#~ class Recipe(db.Model):

    #~ __tablename__ = "recipes"

    #~ id = db.Column(db.Integer, primary_key=True)
    #~ recipe_title = db.Column(db.String, nullable=False)
    #~ recipe_description = db.Column(db.String, nullable=False)
    #~ is_public = db.Column(db.Boolean, nullable=False)
    #~ image_filename = db.Column(db.String, default=None, nullable=True)
    #~ image_url = db.Column(db.String, default=None, nullable=True)
    #~ user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #~ def __init__(self, title, description, user_id, is_public, image_filename=None, image_url=None):
        #~ self.recipe_title = title
        #~ self.recipe_description = description
        #~ self.is_public = is_public
        #~ self.image_filename = image_filename
        #~ self.image_url = image_url
        #~ self.user_id = user_id

    #~ def __repr__(self):
        #~ return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.recipe_title, self.user_id)

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


if __name__ == "__main__":
    # env FLASK_APP=ssp_license_app.py FLASK_DEBUG=1 python -m flask run
    app.run()
