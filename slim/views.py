# -*- coding: utf-8 -*-

import os
import subprocess

from flask import (
    request, redirect, url_for, flash, render_template, make_response)

from flask_security import login_required, current_user
from flask_uploads import UploadNotAllowed

from . import utils
from .app import app, request_uploader
from .models import db, License, User, Product, Purchase


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/licenses')
@login_required
def licenses():
    query = License.query.filter_by(user_id=current_user.id)
    return render_template(
        'licenses.html',
        pagination=query.paginate(per_page=app.config['SLIM_ITEMS_PER_PAGE']),
        products=Product.query,
        target='show_license')


@app.route('/products')
@login_required
def products():
    purchased = Purchase.product_ids(current_user.id)
    purchase_map = dict(
        (prod.id, prod.id in purchased) for prod in Product.query.all())
    return render_template(
        'products.html',
        pagination=Product.query.paginate(
            per_page=app.config['SLIM_ITEMS_PER_PAGE']),
        purchase_map=purchase_map,
        support_link=utils.make_support_link(app.config['SLIM_SUPPORT_EMAIL']))


@app.route('/purchases')
@login_required
def purchases():
    support_link = utils.make_support_link(app.config['SLIM_SUPPORT_EMAIL'])
    return render_template(
        'purchases.html',
        pagination=Purchase.query.filter_by(user_id=current_user.id).paginate(
            per_page=app.config['SLIM_ITEMS_PER_PAGE']),
        products=Product.query,
        support_link=support_link)


def _new_get():
    purchased = Purchase.product_ids(current_user.id)
    products = [
        product for product in Product.query.all() if product.id in purchased]

    if current_user.has_role('admin'):
        users = User.query.all()
    else:
        users = None

    return render_template('new.html', products=products, users=users)


def _new_post():
    # check
    product = request.form['product']
    product = Product.query.filter_by(name=product).first()
    if 'user' in request.form:
        user = request.form['user']
        user = User.query.filter_by(email=user).first()
    else:
        user = current_user

    # Total purchase count for the current user
    tot_purchase_count = Purchase.count(user_id=user.id, product_id=product.id)

    # License count
    license_count = License.query.filter_by(user_id=user.id).count()

    if license_count >= tot_purchase_count:
        flash('No purchased license available for this ptoduct. '
              'Please contact the product support or purchase new '
              'licenses.', 'error')
        return _new_get()

    # upload license request
    try:
        filename = request_uploader.save(request.files['license_req'])
    except UploadNotAllowed as ex:
        flash('Upload not allowed: incorrect file type', 'error')
        return _new_get()
    else:
        flash('Request file uploaded')

    try:
        # load request data
        filename = os.path.join(
            app.config['UPLOADED_REQUESTS_DEST'], filename)
        with open(filename, 'rb') as fd:
            data = fd.read()

        # generate the license file
        licfile = filename + '.lic.dat'
        licgencmd = app.config['SLIM_LICENSE_GENERATOR_CMD']
        licgencmd = utils.expand_cmd_vars(licgencmd,
                                          INPUT_REQUEST_FILE=filename,
                                          OUTPUT_LICENSE_FILE=licfile)

        try:
            subprocess.check_call(licgencmd, shell=False)
        except subprocess.CalledProcessError as ex:
            flash(str(ex), 'error')
            msg = ('Unable to generate license for request %r, please '
                   'check that the input is correct.' %
                   os.path.basename(filename))
            flash(msg, 'error')
            return _new_get()
        else:
            flash('New license correctly generated')

        # load the license data
        with open(licfile, 'rb') as fd:
            licdata = fd.read()
        os.remove(licfile)

        # save the new license
        license = License(
            user_id=user.id,
            product_id=product.id,
            request=data,
            license=licdata,
            description=request.form['description'],
        )

        db.session.add(license)
        db.session.commit()
    finally:
        os.remove(filename)

    return redirect(url_for('licenses'))


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        return _new_post()
    else:
        return _new_get()


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
