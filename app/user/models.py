# coding=utf-8

import datetime as dt
from werkzeug.security import generate_password_hash
from flask import current_app

from app.extensions import es
from app.mixins import ModelMixin


class User(ModelMixin):

    id = None
    es_index = 'user-index'
    doc_type = 'user'

    @classmethod
    def create(cls, username, password) ->dict:

        # 检查 username 是否存在
        res = es.search(
            index=User.es_index, doc_type=User.doc_type,
            body={"query": {"match": {"username": username}}}
        )
        current_app.logger.debug(res)
        hits = res['hits']['hits']
        if len(hits) > 0:
            return None

        # 不存在则创建
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, body=user)
        return res

    @classmethod
    def update(cls, id, username, password):
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, id=id, body=user, refresh=True)
        return res

    @staticmethod
    def init_data():
        admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin'),
            'create_datetime': dt.datetime.now()
        }
        res = es.index(index=User.es_index, doc_type=User.doc_type, id=1, body=admin)
        print(res)
