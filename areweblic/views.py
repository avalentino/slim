# -*- coding: utf-8 -*-

import os
import subprocess

from flask import (
    request, redirect, url_for, flash, render_template, make_response)

from flask_security import login_required, roles_accepted, current_user
from flask_uploads import UploadNotAllowed

from .app import app, request_uploader
from .models import db, License, User, Role, Product


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/licenses')
@login_required
def licenses():
    query = License.query.filter(License.user_id == current_user.id)
    return render_template(
        'licenses.html',
        pagination=query.paginate(per_page=app.config['ITEMS_PER_PAGE']),
        products=Product.query,
        target='show_license')


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

                # product
                name = request.form['product']
                product = Product.query.filter(Product.name == name).first()

                # save the new license
                license = License(
                    current_user.id,
                    product_id=product.id,
                    request=data,
                    license=licdata,
                    description=request.form['description'])

                db.session.add(license)
                db.session.commit()

            os.remove(filename)

            return redirect(url_for('licenses'))

    products = Product.query.all()

    if current_user.has_role('admin'):
        users = User.query.all()
    else:
        users = None

    return render_template('new.html', products=products, users=users)


@app.route('/admin/licenses/<int:lic_id>', endpoint='admin_show_license')
@app.route('/licenses/<int:lic_id>')
@login_required
def show_license(lic_id):
    lic = License.query.get_or_404(lic_id)
    if not current_user.has_role('admin') and lic.user_id != current_user.id:
        # return abort(403)
        flash('You do not have permission to view this resource.', 'error')
        return redirect(url_for('index'))

    user = User.query.get(lic.user_id)
    product = Product.query.get(lic.product_id)
    return render_template('license.html', lic=lic, user=user, product=product)


@app.route('/admin/licenses/<int:lic_id>/download')
@app.route('/licenses/<int:lic_id>/download')
@login_required
def download(lic_id):
    lic = License.query.get_or_404(lic_id)
    if not current_user.has_role('admin') and lic.user_id != current_user.id:
        # return abort(403)
        flash('You do not have permission to view this resource.', 'error')
        return redirect(url_for('index'))

    response = make_response(lic.license)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=lic.dat'

    return response


@app.route('/profile')
@login_required
def user_profile():
    return render_template('user.html', user=current_user)


@app.route('/admin/users/<int:user_id>')
@roles_accepted('admin')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)


@app.route('/admin')
@roles_accepted('admin')
def admin_index():
    return redirect(url_for('index'))


@app.route('/admin/users')
@roles_accepted('admin')
def admin_users():
    return render_template(
        'users.html',
        pagination=User.query.paginate(per_page=app.config['ITEMS_PER_PAGE']))


@app.route('/admin/roles')
@roles_accepted('admin')
def admin_roles():
    return render_template(
        'roles.html',
        pagination=Role.query.paginate(per_page=app.config['ITEMS_PER_PAGE']))


@app.route('/admin/products')
@roles_accepted('admin')
def admin_products():
    return render_template(
        'products.html',
        pagination=Product.query.paginate(
            per_page=app.config['ITEMS_PER_PAGE']))


@app.route('/admin/licenses')
@roles_accepted('admin')
def admin_licenses():
    return render_template(
        'licenses.html',
        pagination=License.query.paginate(
            per_page=app.config['ITEMS_PER_PAGE']),
        users=User.query,
        products=Product.query,
        target='admin_show_license')
