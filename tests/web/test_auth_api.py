# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from .utils import create_user, user_login, get_token


class AuthAPITestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_1_user_login(self):
        """用户登录"""
        create_user(username='admin', password='admin')
        response = user_login(self.client, username='admin', password='admin')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['data']['token'])

    def test_2_user_logout(self):
        """用户登出"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.post(url_for('auth_bp.logout'), data=dict(
            token=token
        ))
        self.assertEqual(response.status_code, 204)
