# -*- coding: utf-8 -*-

"""Admin tools for the SLiM Flask application."""

from __future__ import absolute_import

try:
    from future import standard_library
except ImportError:
    pass
else:
    standard_library.install_aliases()

from collections import Counter

from flask import abort, redirect, request, url_for
from flask_admin import Admin, expose, AdminIndexView as _AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_security import current_user, roles_accepted

import wtforms
from jinja2 import Markup

from . import models
from ._compat import hash_password


__all__ = [
    'ModelView', 'AdminIndexView', 'RoleModelView', 'UserModelView',
    'ProductModelView', 'PurchaseModelView', 'LicenseModelView', 'admin',
]


class AdminIndexView(_AdminIndexView):
    """Generate the view for the main admin page of the SLiM application."""

    @expose()
    @roles_accepted('admin')
    def index(self):
        """Generate the view for the main admin page."""

        return self.render(self._template)


def _format_large_binary_data(data, size=32):
    s = data[:size].decode('utf-8', 'replace')
    if len(data) > size:
        s += ' ...'
    return s


def _format_password(data, size=6, placemark='*'):
    return placemark * size


def large_binary_data_type_formatter(view, value):
    return _format_large_binary_data(value)


_DOWNLOAD_BUTTON_TEMPLATE = '''\
<form style="display: inline;" action='%s' method='get'>
  <button class="btn btn-primary">
    <span class="glyphicon glyphicon-download-alt"></span>
  </button>
</form>'''


def request_data_formatter(view, context, model, name):
    # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name

    target = url_for('admin_download_request_file', lic_id=model.id)

    return Markup(' '.join([
        _format_large_binary_data(model.request),
        _DOWNLOAD_BUTTON_TEMPLATE % target
    ]))


def license_data_formatter(view, context, model, name):
    # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name

    target = url_for('download', lic_id=model.id)

    return Markup(' '.join([
        _format_large_binary_data(model.license),
        _DOWNLOAD_BUTTON_TEMPLATE % target
    ]))


def url_formatter(view, context, model, name):
    # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name

    return Markup('<a href="%(url)s">%(url)s</s>' % dict(url=model.url))


class PasswordInputWidget(wtforms.widgets.PasswordInput):
    def _value(self):
        value = super(PasswordInputWidget, self)._value()
        if value:
            value = hash_password(value)
        return value


class PasswordInputField(wtforms.PasswordField):
    widget = PasswordInputWidget()


class ModelView(sqla.ModelView):
    """Base class for model views."""

    column_display_pk = True
    # column_display_all_relations = True

    column_type_formatters = {
        bytes: large_binary_data_type_formatter,
    }

    def is_accessible(self):
        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class RoleModelView(ModelView):
    """Generate the view for the role model."""

    column_display_all_relations = True
    column_formatters = dict(
        users=lambda v, c, m, p: ', '.join(item.email for item in m.users),
    )
    # column_list = (
    #     'id',
    #     'name',
    #     'description',
    #     'users',
    # )
    form_args = dict(
        name=dict(validators=[wtforms.validators.DataRequired()]),
    )


class UserModelView(ModelView):
    """Generate the view for the user model."""

    # column_display_all_relations = True
    column_formatters = dict(
        password=lambda v, c, m, p: _format_password(m.password),
        roles=lambda v, c, m, p: ', '.join(item.name for item in m.roles),
        purchases=lambda v, c, m, p: ', '.join(
            '%s (%d)' % (p.product.name, p.quantity) for p in m.purchases),
        licenses=lambda v, c, m, p: ', '.join(
            '%s (%d)' % (p, n)
            for p, n in Counter(l.product.name for l in m.licenses).items()),
    )
    column_list = (
        'id',
        'email',
        'password',
        'roles',
        'active',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
        'purchases',
        'licenses',
    )
    column_editable_list = (
        # 'email',
        # 'password',
        # 'roles',
        'active',
    )
    column_filters = (
        'roles',
        'active',
    )
    form_excluded_columns = (
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
    )
    form_overrides = dict(
        password=PasswordInputField,
    )
    form_args = dict(
        email=dict(validators=[wtforms.validators.DataRequired()]),
        roles=dict(validators=[wtforms.validators.DataRequired()]),
    )


class ProductModelView(ModelView):
    """Generate the view for the product model."""

    column_display_all_relations = True
    column_formatters = dict(
        url=url_formatter,
        licenses=lambda v, c, m, p: m.licenses.count(),
        purchases=lambda v, c, m, p: sum(
            item.quantity for item in m.purchases),
    )
    form_args = dict(
        name=dict(validators=[wtforms.validators.DataRequired()]),
    )


class PurchaseModelView(ModelView):
    """Generate the view for the purchase model."""

    # column_display_all_relations = True
    column_list = (
        'id',
        'user',
        'product',
        'quantity',
    )
    column_editable_list = (
        'quantity',
    )
    column_filters = (
        'user',
        'product',
    )
    form_args = dict(
        user=dict(validators=[wtforms.validators.DataRequired()]),
        product=dict(validators=[wtforms.validators.DataRequired()]),
        quantity=dict(validators=[wtforms.validators.DataRequired()]),
    )


class LicenseModelView(ModelView):
    """Generate the view for the license model."""

    can_create = False
    column_formatters = dict(
        request=request_data_formatter,
        license=license_data_formatter,
    )
    column_list = (
        'id',
        'user',
        'product',
        'description',
        'request',
        'request_date',
        'license',
    )
    column_filters = (
        'user',
        'product',
    )
    form_excluded_columns = (
        'request',
        'request_date',
        'license',
    )
    # form_overrides = {
    #     'request': form.FileUploadField,
    #     'license': form.FileUploadField,
    # }
    form_args = dict(
        user=dict(validators=[wtforms.validators.DataRequired()]),
        product=dict(validators=[wtforms.validators.DataRequired()]),
        # request=dict(
        #     'label': 'Request file',
        #     'base_path': current_app.config['UPLOADED_REQUESTS_DEST'],
        #     'allow_overwrite': False
        # )
        # license=dict(
        #     'label': 'License file',
        #     'base_path': current_app.config['UPLOADED_REQUESTS_DEST'],
        #     'allow_overwrite': False
        # )
    )


admin = Admin(
    name='slim',
    index_view=AdminIndexView(name='Admin'),
    base_template='admin/slim_master.html',
    template_mode='bootstrap3',
)

admin.add_view(RoleModelView(models.Role, models.db.session))
admin.add_view(UserModelView(models.User, models.db.session))
admin.add_view(ProductModelView(models.Product, models.db.session))
admin.add_view(PurchaseModelView(models.Purchase, models.db.session))
admin.add_view(LicenseModelView(models.License, models.db.session))

admin.add_link(MenuLink('Home', endpoint='index'))
admin.add_link(MenuLink('Logout', endpoint='security.logout'))
