# coding=utf-8

from werkzeug.security import generate_password_hash

from app.extensions import mongo


class User(object):

    user_id = None
    username = ''
    password_hash = ''

    @staticmethod
    def init_data():
        password_hash = generate_password_hash("admin")
        admin_json = dict(_id=1, username="admin", password_hash=password_hash)
        mongo.db.user.save(admin_json)
