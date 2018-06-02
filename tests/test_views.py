# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import unittest
import contextlib

try:
    from unittest import mock
except ImportError:
    # @COMPATIBILITY: Python < 3.3
    import mock

import flask_testing

os.environ['SLIM_SETTINGS_PATH'] = os.path.join(
    os.path.dirname(__file__), 'slim_testing_config.py')

import slim.app
import slim.models


security = slim.app.components['security']
user_datastore = slim.app.components['user_datastore']


class TestCase(flask_testing.TestCase):
    # render_templates = False

    def create_app(self):
        app = slim.app.app
        # app.config.from_mapping(
        #     TESTING=True,
        #     # LOGIN_DISABLED=True,
        #     SECURITY_PASSWORD_HASH='plaintext',
        #     SQLALCHEMY_DATABASE_URI='sqlite://',
        #     # PRESERVE_CONTEXT_ON_EXCEPTION=False,
        # )

        return app

    def setUp(self):
        # slim.models.db.create_all()

        slim.app.init_db(self.app, user_datastore, password='admin')

        self.admin = user_datastore.find_user(email='admin')
        user_datastore.activate_user(self.admin)

        role = user_datastore.find_role('user')
        self.user = user_datastore.create_user(email='user0', password='user0')
        user_datastore.add_role_to_user(self.user, role)
        user_datastore.activate_user(self.user)

    def tearDown(self):
        del self.admin
        del self.user
        slim.models.db.session.remove()
        slim.models.db.drop_all()

    @contextlib.contextmanager
    def login(self, user):
        import flask_login

        self.app.login_manager._login_disabled = True

        if hasattr(flask_login, '_get_user'):
            mock_get_user = mock.patch('flask_login._get_user',
                                       mock.Mock(return_value=user))
        else:
            mock_get_user = mock.patch('flask_login.utils._get_user',
                                       mock.Mock(return_value=user))

        with mock_get_user:
            yield

        self.app.login_manager._login_disabled = False


class TestUserViews01(TestCase):
    send_button_text = (
        '<span class="glyphicon glyphicon-envelope"></span> Send')
    new_license_button_text = (
        '<span class="glyphicon glyphicon-upload"></span> New license request')

    def test_index(self):
        with self.login(self.user):
            response = self.client.get('/')
            self.assert_200(response)
            self.assert_template_used('index.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('products' in data)
            self.assertTrue('licenses' in data)
            self.assertTrue('purchases' in data)
            self.assertTrue('new' in data)
            self.assertFalse('admin' in data)

    def test_products(self):
        with self.login(self.user):
            response = self.client.get('/products')
            self.assert_200(response)
            self.assert_template_used('products.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('products' in data)
            self.assertTrue('count' in data)
            self.assertTrue('no product found.' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_licenses(self):
        with self.login(self.user):
            response = self.client.get('/licenses')
            self.assert_200(response)
            self.assert_template_used('licenses.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('licenses' in data)
            self.assertTrue('count' in data)
            self.assertTrue('no license found.' in data)
            self.assertTrue(self.new_license_button_text.lower() in data)

    def test_purchases(self):
        with self.login(self.user):
            response = self.client.get('/purchases')
            self.assert_200(response)
            self.assert_template_used('purchases.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('purchases' in data)
            self.assertTrue('count' in data)
            self.assertTrue('no purchase found.' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_new_get(self):
        with self.login(self.user):
            response = self.client.get('/new')
            self.assert_200(response)
            self.assert_template_used('new.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('submit a new license request' in data)
            self.assertTrue('product' in data)
            self.assertTrue('request file' in data)
            self.assertTrue(
                '<form class="form" action="/new" method="post"' in data)
            self.assertTrue('<input type=file' in data)
            self.assertTrue(
                '<button type="reset">Reset</button>'.lower() in data)
            self.assertTrue(
                '<button type="submit">Submit</button>'.lower() in data)

    def test_about(self):
        with self.login(self.user):
            response = self.client.get('/about')
            self.assert_200(response)
            self.assert_template_used('about.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('about' in data)
            self.assertTrue('slim' in data)

    def test_profile(self):
        with self.login(self.user):
            response = self.client.get('/profile')
            self.assert_200(response)
            self.assert_template_used('user.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue(('User "%s"' % self.user.email).lower() in data)
            self.assertTrue('id' in data)
            self.assertTrue('email' in data)
            self.assertTrue('active' in data)
            self.assertTrue('roles' in data)
            self.assertTrue('login count' in data)
            self.assertTrue('current login at' in data)
            self.assertTrue('current login ip' in data)
            self.assertTrue('last login at' in data)
            self.assertTrue('last login ip' in data)
            self.assertTrue('password' in data)

    def test_invalid(self):
        with self.login(self.user):
            response = self.client.get('/invalid_url', follow_redirects=True)
            self.assert_404(response)

    def test_admin_invalid(self):
        with self.login(self.user):
            response = self.client.get('/admin/invalid_url',
                                       follow_redirects=True)
            self.assert_404(response)

    def test_admin_01(self):
        with self.login(self.user):
            response = self.client.get('/admin/')
            self.assertTrue(response.status_code in (301, 302))

    def test_admin_02(self):
        with self.login(self.user):
            response = self.client.get('/admin/', follow_redirects=True)
            self.assert_200(response)
            self.assert_message_flashed(
                'You do not have permission to view this resource.', 'error')

    def test_admin_roles(self):
        with self.login(self.user):
            response = self.client.get('/admin/role', follow_redirects=True)
            self.assert_403(response)

    def test_admin_users(self):
        with self.login(self.user):
            response = self.client.get('/admin/user', follow_redirects=True)
            self.assert_403(response)

    def test_admin_products(self):
        with self.login(self.user):
            response = self.client.get('/admin/product', follow_redirects=True)
            self.assert_403(response)

    def test_admin_purchases(self):
        with self.login(self.user):
            response = self.client.get('/admin/purchase', follow_redirects=True)
            self.assert_403(response)

    def test_admin_licenses(self):
        with self.login(self.user):
            response = self.client.get('/admin/license', follow_redirects=True)
            self.assert_403(response)

    def test_license_01(self):
        with self.login(self.user):
            response = self.client.get('/licenses/400')
            self.assert_404(response)


class TestUserViews02(TestUserViews01):
    license_download_button = (
        '<button class="btn btn-primary">'
        '<span class="glyphicon glyphicon-download-alt"></span> '
        'Download</button>')

    def setUp(self):
        super(TestUserViews02, self).setUp()

        from slim.__main__ import _init_test_db
        _init_test_db()

        self.user = user_datastore.find_user(email='user1')

    def test_products(self):
        with self.login(self.user):
            response = self.client.get('/products')
            self.assert_200(response)
            self.assert_template_used('products.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('products' in data)
            self.assertTrue('count' in data)
            self.assertTrue('description' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_licenses(self):
        with self.login(self.user):
            response = self.client.get('/licenses')
            self.assert_200(response)
            self.assert_template_used('licenses.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('licenses' in data)
            self.assertTrue('count' in data)
            self.assertTrue('request date' in data)
            self.assertTrue(self.new_license_button_text.lower() in data)

    def test_purchases(self):
        with self.login(self.user):
            response = self.client.get('/purchases')
            self.assert_200(response)
            self.assert_template_used('purchases.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('purchases' in data)
            self.assertTrue('count' in data)
            self.assertTrue('quantity' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_license_02(self):
        with self.login(self.user):
            license = self.user.licenses.first()
            product = license.product

            response = self.client.open('/licenses/%d' % license.id)
            self.assert_200(response)
            self.assert_template_used('license.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue(('License n. %d' % license.id).lower() in data)
            self.assertTrue('user' in data)
            self.assertTrue(self.user.email in data)
            self.assertTrue('product' in data)
            self.assertTrue(product.name.lower() in data)
            self.assertTrue('description' in data)
            if license.description is not None:
                self.assertTrue(license.description.lower() in data)
            self.assertTrue('request date' in data)
            self.assertTrue('download' in data)
            self.assertTrue(self.license_download_button.lower() in data)

    def test_license_03(self):
        with self.login(self.user):
            response = self.client.get('/licenses/1', follow_redirects=True)
            self.assert_200(response)
            self.assert_message_flashed(
                'You do not have permission to view this resource.', 'error')


class AdminTestMixin:
    def test_index(self):
        with self.login(self.user):
            response = self.client.get('/')
            self.assert_200(response)
            self.assert_template_used('index.html')

            data = response.get_data(as_text=True).lower()
            self.assertTrue('products' in data)
            self.assertTrue('licenses' in data)
            self.assertTrue('purchases' in data)
            self.assertTrue('new' in data)
            self.assertTrue('admin' in data)

    def test_admin_01(self):
        with self.login(self.user):
            response = self.client.get('/admin/')
            self.assert_200(response)

    def test_admin_02(self):
        with self.login(self.user):
            response = self.client.get('/admin/')
            self.assert_200(response)
            self.assertFalse(self.flashed_messages)

    def test_admin_roles(self):
        with self.login(self.user):
            response = self.client.get('/admin/role', follow_redirects=True)
            self.assert_200(response)
            data = response.get_data(as_text=True)
            self.assertTrue('<title>Role - SLiM</title>')

    def test_admin_users(self):
        with self.login(self.user):
            response = self.client.get('/admin/user', follow_redirects=True)
            self.assert_200(response)
            data = response.get_data(as_text=True)
            self.assertTrue('<title>User - SLiM</title>')

    def test_admin_products(self):
        with self.login(self.user):
            response = self.client.get('/admin/product', follow_redirects=True)
            self.assert_200(response)
            data = response.get_data(as_text=True)
            self.assertTrue('<title>Product - SLiM</title>')

    def test_admin_purchases(self):
        with self.login(self.user):
            response = self.client.get('/admin/purchase', follow_redirects=True)
            self.assert_200(response)
            data = response.get_data(as_text=True)
            self.assertTrue('<title>Purchase - SLiM</title>')

    def test_admin_licenses(self):
        with self.login(self.user):
            response = self.client.get('/admin/license', follow_redirects=True)
            self.assert_200(response)
            data = response.get_data(as_text=True)
            self.assertTrue('<title>License - SLiM</title>')


class TestAdminViews01(AdminTestMixin, TestUserViews01):
    def setUp(self):
        super(TestAdminViews01, self).setUp()
        self.user = self.admin


class TestAdminViews02(AdminTestMixin, TestUserViews02):
    def setUp(self):
        super(TestAdminViews02, self).setUp()
        self.user = self.admin

    def test_license_03(self):
       with self.login(self.user):
           response = self.client.get('/licenses/1')
           self.assert_200(response)


if __name__ == '__main__':
    unittest.main()
