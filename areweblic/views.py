# -*- coding: utf-8 -*-

import os
import subprocess

from flask import (
    request, redirect, url_for, flash, render_template, make_response)

from flask_uploads import UploadNotAllowed

from .app import app, db, request_uploader
from .models import License


@app.route('/')
def index():
    return render_template('index.html', count=License.query.count())


@app.route('/licenses')
def licenses():
    return render_template('licenses.html', items=License.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST' and 'license_req' in request.files:
        if not request.files['license_req']:
            flash('"Request file" fiield not set', 'error')

        try:
            filename = request_uploader.save(request.files['license_req'])
        except UploadNotAllowed as ex:
            flash('Upload not allowed: incorrect file type', 'error')
        else:
            flash('Request file uploaded')

            # load request data
            filename = os.path.join(
                app.config['UPLOADED_REQUESTS_DEST'], filename)
            with open(filename, 'rb') as fd:
                data = fd.read()

            # generate the license file
            bin = app.config['LICENSE_GENERATOR_PATH']
            licfile = filename + '.lic.dat'
            args = [bin, 'add', filename, licfile]
            try:
                subprocess.check_call(args, shell=False)
            except subprocess.CalledProcessError as ex:
                msg = ('Unable to generate license for request %r, please '
                       'check that the input is correct.' %
                       os.basename(filename))
                flash(msg, 'error')
            else:
                flash('New license correctly generated')

                # load the license data
                with open(licfile, 'rb') as fd:
                    licdata = fd.read()
                os.remove(licfile)

                # save the new license
                req = License(
                    'user_id',  # XXX
                    product=request.form['product'],
                    request=data,
                    license=licdata,
                    description=request.form['description'])

                db.session.add(req)
                db.session.commit()

            os.remove(filename)

            return redirect(url_for('licenses'))
    return render_template('new.html')


@app.route('/license/<int:req_id>')
def show_license(req_id):
    req = License.query.get(req_id)
    return render_template('license.html', req=req)


@app.route('/download/<int:req_id>')
def download(req_id):
    req = License.query.get(req_id)
    data = req.license

    response = make_response(data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=lic.dat'

    return response
