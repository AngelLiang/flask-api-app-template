# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from tests.web.utils import create_user, get_token, gen_auth_headers


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
        response = self.client.post(
            url_for('user_token_bp.users_token_api'),
            json=dict(username='admin', password='admin')
        )
        data = response.get_json()
        # print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(data['data']['token'])

    def test_2_delete_user_token(self):
        """清除用户token"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.delete(
            url_for('user_token_bp.users_token_api'),
            headers=gen_auth_headers(token, is_json=False)
        )
        # print(response.json)
        self.assertEqual(response.status_code, 204)

    def test_3_auth_token_in_header(self):
        """测试放在header里的token"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.delete(
            url_for('user_token_bp.users_token_api'),
            headers=gen_auth_headers(token, is_json=False)
        )
        self.assertEqual(response.status_code, 204)

    def test_4_auth_token_in_query_string(self):
        """测试放在query string里的token"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.delete(
            url_for('user_token_bp.users_token_api', token=token),
        )
        self.assertEqual(response.status_code, 204)

    def test_5_auth_token_in_json(self):
        """测试放在json里的token"""
        create_user(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.delete(
            url_for('user_token_bp.users_token_api'),
            json=dict(token=token, token_type='Bearer')
        )
        # print(response.json)
        self.assertEqual(response.status_code, 204)
