# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from tests.web.utils import create_user, get_token


class UserTokenAPITestCase(unittest.TestCase):
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

    def test_1_get_user_token(self):
        """获取用户token"""
        create_user(username='admin', password='admin')
        response = self.client.post(url_for('user_token_bp.user_token_api'), data=dict(
            username='admin',
            password='admin'
        ))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['token'])

    def test_2_delete_user_token(self):
        """清除用户token"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.delete(url_for('user_token_bp.user_token_api'), data=dict(
            token=token
        ))
        self.assertEqual(response.status_code, 200)
