# -*- coding: utf-8 -*-

from flask import abort, redirect, request, url_for
from flask_admin import Admin, expose, AdminIndexView as _AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_security import current_user, roles_accepted

from . import models


class AdminIndexView(_AdminIndexView):
    @expose()
    @roles_accepted('admin')
    def index(self):
        return self.render(self._template)


def _format_large_binary_data(data, size=10):
    s = data[:size].decode('utf-8', 'replace')
    if len(data) > size:
        s += ' ...'
    return s


def _format_password(data, size=6, placemark='*'):
    return placemark * size


def large_binary_data_formatter(view, value):
    return _format_large_binary_data(value)


class ModelView(sqla.ModelView):
    column_type_formatters = {
        bytes: large_binary_data_formatter,
    }
    column_display_pk = True
    # column_display_all_relations = True

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


class UserModelView(ModelView):
    column_formatters = dict(
        password=lambda v, c, m, p: _format_password(m.password),
    )
    column_display_all_relations = True
    column_list = (
        'id',
        'email',
        'password',
        'active',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
        'roles',
    )


class PurchaseModelView(ModelView):
    column_auto_select_related = True
    column_display_all_relations = True
    column_list = ('id', 'user_id', 'product_id', 'quantity')


class LicenseModelView(ModelView):
    column_auto_select_related = True
    column_display_all_relations = True
    column_list = (
        'id',
        'user_id',
        'product_id',
        'description',
        'request',
        'request_date',
        'license',
    )


admin = Admin(
    name='slim',
    index_view=AdminIndexView(name='Admin'),
    base_template='admin/slim_master.html',
    template_mode='bootstrap3',
)

admin.add_view(ModelView(models.Role, models.db.session))
admin.add_view(UserModelView(models.User, models.db.session))
admin.add_view(ModelView(models.Product, models.db.session))
admin.add_view(PurchaseModelView(models.Purchase, models.db.session))
admin.add_view(LicenseModelView(models.License, models.db.session))

admin.add_link(MenuLink('Home', endpoint='index'))
admin.add_link(MenuLink('Logout', endpoint='security.logout'))
