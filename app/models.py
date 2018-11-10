# coding=utf-8

from werkzeug.security import generate_password_hash

from app.extensions import es


class ModelMixin(object):
    """
    必须实现`es_index`和`doc_type`属性。
    """

    @classmethod
    def get(cls, id):
        res = es.get(index=cls.es_index, doc_type=cls.doc_type, id=id)
        return res

    @classmethod
    def create(cls, **kw):
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, id=id, body=kw)
        return res

    @classmethod
    def update(cls, id, *args, **kw):
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, id=id, body=kw)
        return res

    @classmethod
    def delete(cls, id):
        res = es.delete(index=cls.es_index, doc_type=cls.doc_type, id=id)
        return res


class User(ModelMixin):

    id = None
    es_index = 'user-index'
    doc_type = 'user'

    @classmethod
    def create(cls, username, password, id=None):
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, id=id, body=user)
        return res

    @classmethod
    def update(cls, id, username, password):
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
        }
        res = es.update(index=cls.es_index, doc_type=cls.doc_type, id=id, body=user)
        return res

    @staticmethod
    def init_data():
        admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin'),
        }
        res = es.index(index=User.es_index, doc_type=User.doc_type, id=1, body=admin)
        print(res['result'])
