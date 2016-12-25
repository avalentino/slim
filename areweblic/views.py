# -*- coding: utf-8 -*-

import os
import subprocess

from flask import (
    request, redirect, url_for, flash, render_template, make_response)

from flask_security import login_required, roles_accepted, current_user
from flask_uploads import UploadNotAllowed

from .app import app, db, request_uploader
from .models import License, User, Role


@app.route('/')
@login_required
def index():
    query = License.query.filter(License.user_id == current_user.id)
    return render_template('index.html', count=query.count())


@app.route('/licenses')
@login_required
def licenses():
    query = License.query.filter(License.user_id == current_user.id)
    return render_template('licenses.html', pagination=query.paginate())


@app.route('/new', methods=['GET', 'POST'])
@login_required
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
                license = License(
                    current_user.id,
                    product=request.form['product'],
                    request=data,
                    license=licdata,
                    description=request.form['description'])

                db.session.add(license)
                db.session.commit()

            os.remove(filename)

            return redirect(url_for('licenses'))
    return render_template('new.html')


@app.route('/licenses/<int:lic_id>')
@login_required
def show_license(lic_id):
    if current_user.has_role('admin'):
        query = License.query
    else:
        query = License.query.filter(License.user_id == current_user.id)
    lic = query.get(lic_id)
    user = User.query.filter(User.id == lic.user_id).first()
    return render_template('license.html', lic=lic, user=user)


@app.route('/download/<int:lic_id>')
@login_required
def download(lic_id):
    if current_user.has_role('admin'):
        query = License.query
    else:
        query = License.query.filter(License.user_id == current_user.id)
    data = query.get(lic_id).license

    response = make_response(data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=lic.dat'

    return response


@app.route('/admin/users')
@roles_accepted('admin')
def admin_users():
    return render_template('users.html', pagination=User.query.paginate())


@app.route('/admin/roles')
@roles_accepted('admin')
def admin_roles():
    return render_template('roles.html', pagination=Role.query.paginate())


@app.route('/admin/licenses')
@roles_accepted('admin')
def admin_licenses():
    return render_template(
        'licenses.html', pagination=License.query.paginate(), users=User.query)
