# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import mock
import unittest
import contextlib

import flask_testing
from flask_security import current_user, login_user

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
        #     TESTING=self.TESTING,
        #     SECURITY_PASSWORD_HASH='plaintext',
        #     SQLALCHEMY_DATABASE_URI=self.SQLALCHEMY_DATABASE_URI,
        # )

        return app

    def setUp(self):
        # slim.models.db.create_all()

        slim.app.init_db(self.app, user_datastore, password='admin')

        self.admin = user_datastore.find_user(email='admin')
        user_datastore.activate_user(self.admin)

        role = user_datastore.find_role('user')
        self.user = user_datastore.create_user(email='user', password='user')
        user_datastore.add_role_to_user(self.user, role)
        user_datastore.activate_user(self.user)

    def tearDown(self):
        del self.admin
        del self.user
        slim.models.db.session.remove()
        slim.models.db.drop_all()

    @contextlib.contextmanager
    def login(self, user):
        mock_get_user = mock.patch('flask_login._get_user',
                                   mock.Mock(return_value=user))
        self.app.login_manager._login_disabled = True
        mock_get_user.start()
        yield
        mock_get_user.stop()
        self.app.login_manager._login_disabled = False


class TestUserViews01(TestCase):
    send_button_text = (
        b'<span class="glyphicon glyphicon-envelope"></span> Send')
    new_license_button_text = (
        b'<span class="glyphicon glyphicon-upload"></span> New license request')

    def test_index(self):
        with self.login(self.user):
            response = self.client.get('/')
            self.assert_200(response)
            self.assert_template_used('index.html')

            data = response.data.lower()
            self.assertTrue(b'products' in data)
            self.assertTrue(b'licenses' in data)
            self.assertTrue(b'purchases' in data)
            self.assertTrue(b'new' in data)
            self.assertFalse(b'admin' in data)

    def test_products(self):
        with self.login(self.user):
            response = self.client.get('/products')
            self.assert_200(response)
            self.assert_template_used('products.html')

            data = response.data.lower()
            self.assertTrue(b'products' in data)
            self.assertTrue(b'count' in data)
            # self.assertTrue(b'description' in data)
            self.assertTrue(b'no product found.' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_licenses(self):
        with self.login(self.user):
            response = self.client.get('/licenses')
            self.assert_200(response)
            self.assert_template_used('licenses.html')

            data = response.data.lower()
            self.assertTrue(b'licenses' in data)
            self.assertTrue(b'count' in data)
            # self.assertTrue(b'request date' in data)
            self.assertTrue(b'no license found.' in data)
            self.assertTrue(self.new_license_button_text.lower() in data)

    def test_purchases(self):
        with self.login(self.user):
            response = self.client.get('/purchases')
            self.assert_200(response)
            self.assert_template_used('purchases.html')

            data = response.data.lower()
            self.assertTrue(b'purchases' in data)
            self.assertTrue(b'count' in data)
            # self.assertTrue(b'quantity' in data)
            self.assertTrue(b'no purchase found.' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_new(self):
        with self.login(self.user):
            response = self.client.get('/new')
            self.assert_200(response)
            self.assert_template_used('new.html')

            data = response.data.lower()
            self.assertTrue(b'submit a new license request' in data)
            self.assertTrue(b'product' in data)
            self.assertTrue(b'request file' in data)
            self.assertTrue(
                b'<form class="form" action="/new" method="post"' in data)
            self.assertTrue(b'<input type=file' in data)
            self.assertTrue(
                b'<button type="reset">Reset</button>'.lower() in data)
            self.assertTrue(
                b'<button type="submit">Submit</button>'.lower() in data)

    def test_profile(self):
        with self.login(self.user):
            response = self.client.get('/profile')
            self.assert_200(response)
            self.assert_template_used('user.html')

            data = response.data.lower()
            self.assertTrue(b'User "user'.lower() in data)
            self.assertTrue(b'id' in data)
            self.assertTrue(b'email' in data)
            self.assertTrue(b'active' in data)
            self.assertTrue(b'roles' in data)
            self.assertTrue(b'login count' in data)
            self.assertTrue(b'current login at' in data)
            self.assertTrue(b'current login ip' in data)
            self.assertTrue(b'last login at' in data)
            self.assertTrue(b'last login ip' in data)
            self.assertTrue(b'password' in data)

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
            response = self.client.get('/admin')
            self.assertTrue(response.status_code in (301, 302))

    def test_admin_02(self):
        with self.login(self.user):
            response = self.client.get('/admin', follow_redirects=True)
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
            response = self.client.get('/license/400')
            self.assert_404(response)


class TestUserViews02(TestUserViews01):
    license_download_button = (
        b'<button class="btn btn-primary">'
        b'<span class="glyphicon glyphicon-download-alt"></span>'
        b' Download</button>')

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

            data = response.data.lower()
            self.assertTrue(b'products' in data)
            self.assertTrue(b'count' in data)
            self.assertTrue(b'description' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_licenses(self):
        with self.login(self.user):
            response = self.client.get('/licenses')
            self.assert_200(response)
            self.assert_template_used('licenses.html')

            data = response.data.lower()
            self.assertTrue(b'licenses' in data)
            self.assertTrue(b'count' in data)
            self.assertTrue(b'request date' in data)
            self.assertTrue(self.new_license_button_text.lower() in data)

    def test_purchases(self):
        with self.login(self.user):
            response = self.client.get('/purchases')
            self.assert_200(response)
            self.assert_template_used('purchases.html')

            data = response.data.lower()
            self.assertTrue(b'purchases' in data)
            self.assertTrue(b'count' in data)
            self.assertTrue(b'quantity' in data)
            self.assertTrue(self.send_button_text.lower() in data)

    def test_license_02(self):
        with self.login(self.user):
            license = self.user.licenses.first()
            product = license.product

            response = self.client.get('/license/%d' % license.id)
            self.assert_200(response)
            self.assert_template_used('license.html')


            data = response.data.lower()
            self.assertTrue((b'License n. %d' % license.id).lower() in data)
            self.assertTrue(b'user' in data)
            self.assertTrue(self.user.email.encode('utf-8') in data)
            self.assertTrue(b'product' in data)
            self.assertTrue(product.name.lower().encode('utf-8') in data)
            self.assertTrue(b'description' in data)
            if license.description is not None:
                self.assertTrue(
                    license.description.lower().encode('utf-8') in data)
            self.assertTrue(b'request date' in data)
            self.assertTrue(b'download' in data)
            self.assertTrue(self.license_download_button.lower() in data)

    def test_license_03(self):
        with self.login(self.user):
            response = self.client.get('/license/1', follow_redirects=True)
            self.assert_200(response)
            self.assert_message_flashed(
                'You do not have permission to view this resource.', 'error')


if __name__ == '__main__':
    unittest.main()
