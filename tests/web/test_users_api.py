# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from tests.web.utils import create_admin, create_user
from tests.web.utils import get_token, gen_auth_headers


class UsersAPITestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_1_get_a_list_of_users(self):
        """管理员获取用户列表"""
        create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.get(
            url_for('user_bp.users_api'),
            headers=gen_auth_headers(token, is_json=False)
        )
        self.assertEqual(response.status_code, 200)

    def test_2_create_a_single_user(self):
        """管理员创建新用户"""
        create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.post(url_for('user_bp.users_api'), json=dict(
            username='user',
            password='user'
        ), headers=gen_auth_headers(token))
        self.assertEqual(response.status_code, 201)

    def test_3_get_a_single_user(self):
        """管理员获取用户详情"""
        admin = create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.get(url_for(
            'user_bp.users_with_id_api', user_id=admin.id), json=dict(
        ), headers=gen_auth_headers(token))
        self.assertEqual(response.status_code, 200)

    def test_4_change_a_single_user(self):
        """管理员修改用户详情"""
        admin = create_admin(username='admin', password='admin')
        token = get_token(self.client, username='admin', password='admin')
        response = self.client.put(url_for(
            'user_bp.users_with_id_api', user_id=admin.id),
            json=dict(fullname='fullname', description='description'),
            headers=gen_auth_headers(token)
        )
        # print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data']['fullname'], 'fullname')
        self.assertEqual(response.json['data']['description'], 'description')
