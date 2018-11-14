# coding=utf-8

import unittest

from flask import url_for
from app.models import User

from app import create_app, db


class APIUserTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()

        user = User()
        user.username = 'admin'
        user.set_password('admin')

        user2 = User()
        user2.username = 'admin02'
        user2.set_password('admin02')

        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def get_token(self):
        response = self.client.post(url_for('api_v1.login'), data=dict(
            username='admin',
            password='admin'
        ))
        data = response.get_json()
        return data['data']['token']

    def test_1_user_list(self):
        response = self.client.get(url_for('api_v1.user_api'), data=dict(
            token=self.get_token()
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_2_user_post(self):
        response = self.client.post(url_for('api_v1.user_api'), data=dict(
            token=self.get_token(),
            username='admin03',
            password='admin03'
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_3_user_id_get(self):
        response = self.client.get(url_for('api_v1.user_id_api', user_id=1), data=dict(
            token=self.get_token()
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_4_user_id_post(self):
        response = self.client.post(
            url_for('api_v1.user_id_api', user_id=1),
            data=dict(
                token=self.get_token(),
                # username='admin03',
                password='123456'
            ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)

    def test_5_user_id_delete(self):
        response = self.client.delete(url_for('api_v1.user_id_api', user_id=1), data=dict(
            token=self.get_token()
        ))
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 20000)
