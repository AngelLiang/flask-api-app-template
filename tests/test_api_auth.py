# coding=utf-8

import unittest

from flask import url_for
from app.models import User

from app import create_app


class APIAuthTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()

        User.init_data()

    def tearDown(self):
        self.app_context.pop()

    def get_token(self):
        response = self.client.post(url_for('api_v1.login'), data=dict(
            username='admin',
            password='admin'
        ))
        data = response.get_json()
        return data['data']['token']

    def test_1_login(self):
        response = self.client.post(url_for('api_v1.login'), data=dict(
            username='admin',
            password='admin'
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)
        self.assertIsNotNone(data['data']['token'])

    def test_2_logout(self):
        token = self.get_token()
        response = self.client.post(url_for('api_v1.logout'), data=dict(
            token=token
        ))
        data = response.get_json()
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)
