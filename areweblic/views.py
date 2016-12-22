# -*- coding: utf-8 -*-

import os

from flask import (
    request, redirect, url_for, flash, render_template, make_response)

from flask_uploads import UploadNotAllowed

from . import config
from .app import app, db, request_uploader
from .models import LicenseRequest


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
            filename = request_uploader.save(request.files['license_req'])
        except UploadNotAllowed as ex:
            flash('Upload not allowed: incorrect file type', 'error')
        else:
            flash('Request file saved to %r.' % filename)

            filename = os.path.join(config.UPLOADED_REQUESTS_DEST, filename)
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
    # data = req.license     # XXX
    data = req.request

    response = make_response(data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=lic.dat'

    return response
