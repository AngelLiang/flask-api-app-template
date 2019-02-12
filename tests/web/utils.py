# coding=utf-8

# import unittest

from flask import url_for

# from apps.web import create_app
from apps.web.extensions import db
from apps.web.user.models import User


def create_admin(username='admin', password='admin'):
    user = User()
    user.username = username
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def create_user(username='user', password='user'):
    user = User()
    user.username = username
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def user_login(client, username='admin', password='admin'):
    return client.post(url_for('auth_bp.login'), data=dict(
        username=username,
        password=password
    ))


def get_token(client, username='admin', password='admin'):
    response = client.post(url_for('auth_bp.login'), data=dict(
        username=username,
        password=password
    ))
    json_data = response.get_json()
    # print(json_data)
    return json_data['data']['token']


def gen_auth_headers(token, auth_type='token'):
    return {
        'Authorization': auth_type + ' ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
