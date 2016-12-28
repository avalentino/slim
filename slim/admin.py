# -*- coding: utf-8 -*-

from flask import abort, redirect, request, url_for
from flask_admin import Admin, expose, AdminIndexView as _AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_security import current_user, roles_accepted

from . import models


class ModelView(sqla.ModelView):
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
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminIndexView(_AdminIndexView):
    @expose()
    @roles_accepted('admin')
    def index(self):
        return self.render(self._template)


admin = Admin(
    name='slim',
    index_view=AdminIndexView(name='Admin'),
    base_template='admin/slim_master.html',
    template_mode='bootstrap3',
)

admin.add_link(MenuLink('Home', endpoint='index'))
admin.add_link(MenuLink('Logout', endpoint='security.logout'))

admin.add_view(ModelView(models.Role, models.db.session))
admin.add_view(ModelView(models.User, models.db.session))
admin.add_view(ModelView(models.Product, models.db.session))
admin.add_view(ModelView(models.Purchase, models.db.session))
admin.add_view(ModelView(models.License, models.db.session))
