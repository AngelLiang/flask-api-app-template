# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from tests.web.utils import create_admin, create_user, get_token, gen_auth_headers


class UsersAPITestCase(unittest.TestCase):
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

    def test_1_get_user_list(self):
        """获取用户列表"""
        create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.get(url_for(
            'user_bp.users_api'),
            headers=gen_auth_headers(token)
        )
        # print(response.json)
        self.assertEqual(response.status_code, 200)

    def test_2_create_user(self):
        """创建用户"""
        create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.post(url_for(
            'user_bp.users_api'),
            headers=gen_auth_headers(token),
            json=dict(username='user', password='user')
        )
        # print(response.json)
        self.assertEqual(response.status_code, 201)
