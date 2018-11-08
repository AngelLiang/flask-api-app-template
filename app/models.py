# coding=utf-8

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

Model = db.Model
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String


class User(Model):
    '''User Model'''
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128))

    @property
    def id(self):
        return self.user_id

    @id.setter
    def id(self, val):
        self.user_id = val

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        d = dict(id=self.user_id, username=self.username)
        return d

    @staticmethod
    def init_data():
        admin = User()
        admin.username = 'admin'
        admin.set_password('admin')
        db.session.add(admin)

        admin01 = User()
        admin01.username = 'admin01'
        admin01.set_password('admin01')
        db.session.add(admin01)

        admin02 = User()
        admin02.username = 'admin02'
        admin02.set_password('admin02')
        db.session.add(admin02)

        db.session.commit()
