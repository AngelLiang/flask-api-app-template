# coding=utf-8

# import unittest

from flask import url_for

# from apps.web import create_app
from apps.web.extensions import db
from apps.web.user.models import User


class TestUtil(object):
    """测试用例辅助工具"""

    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_user(username, password):
        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, username='admin', password='admin'):
        return self.client.post(url_for('auth_bp.login'), data=dict(
            username=username,
            password=password
        ))

    def get_token(self, username='admin', password='admin'):
        response = self.client.post(url_for('auth_bp.login'), data=dict(
            username=username,
            password=password
        ))
        json_data = response.get_json()
        # print(json_data)
        return json_data['data']['token']
