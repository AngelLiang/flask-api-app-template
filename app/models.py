# coding=utf-8

from werkzeug.security import generate_password_hash

from app.extensions import es


class User(object):

    @staticmethod
    def init_data():
        admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin'),
        }
        res = es.index(index="user-index", doc_type='user', id=1, body=admin)
        print(res['result'])
