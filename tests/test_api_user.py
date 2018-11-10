# coding=utf-8

import unittest

from flask import url_for
from app.models import User

from app import create_app


class APIUserTestCase(unittest.TestCase):

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

    def test_1_user_list(self):
        response = self.client.get(url_for('api_v1.user_api'))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_2_user_post(self):
        response = self.client.post(url_for('api_v1.user_api'), data=dict(
            username='admin03',
            password='admin03'
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_3_user_id_get(self):
        response = self.client.get(url_for('api_v1.user_id_api', user_id=1))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_4_user_id_post(self):
        response = self.client.post(
            url_for('api_v1.user_id_api', user_id=1),
            data=dict(
                # username='admin03',
                password='123456'
            ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_5_user_id_delete(self):
        response = self.client.delete(url_for('api_v1.user_id_api', user_id=1))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)
