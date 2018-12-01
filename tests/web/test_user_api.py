# coding=utf-8

import unittest

from flask import url_for

from apps.web import create_app
from apps.web.extensions import db
# from apps.web.user.models import User

from .utils import TestUtil


class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()

        self.util = TestUtil(self.client)

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_1_get_user_list(self):
        '''获取用户列表'''
        self.util.create_user(username='admin', password='admin')
        token = self.util.get_token(username='admin', password='admin')
        response = self.client.get(url_for('user_bp.user_api'), data=dict(
            token=token
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_2_get_user_detail(self):
        '''获取用户详情'''
        user = self.util.create_user(username='admin', password='admin')
        token = self.util.get_token(username='admin', password='admin')
        response = self.client.get(url_for('user_bp.user_id_api', id_=user.id), data=dict(
            token=token,
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)
