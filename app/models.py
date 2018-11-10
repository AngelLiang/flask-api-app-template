# coding=utf-8

from werkzeug.security import generate_password_hash

from app.extensions import es


class User(object):

    @classmethod
    def get(cls, user_id):
        res = es.get(index="user-index", doc_type='user', id=user_id)
        return res

    @classmethod
    def create(cls, username, password, user_id=None):
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.index(index="user-index", doc_type='user', id=user_id, body=user)
        return res

    @classmethod
    def update(cls, user_id, username, password):
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.update(index="user-index", doc_type='user', id=user_id, body=user)
        return res

    @classmethod
    def delete(cls, user_id):
        res = es.delete(index="user-index", doc_type='user', id=user_id)
        return res

    @staticmethod
    def init_data():
        admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin'),
        }
        res = es.index(index="user-index", doc_type='user', id=1, body=admin)
        print(res['result'])
