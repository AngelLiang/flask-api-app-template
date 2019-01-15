# coding=utf-8

# import os
import datetime as dt

from werkzeug.security import generate_password_hash, check_password_hash

from apps.web.extensions import db


Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime


class User(Model):
    """帐户"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    create_datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    @property
    def id(self):
        return self.user_id

    @id.setter
    def id(self, value):
        self.user_id = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        d = dict(
            id=self.user_id,
            username=self.username,
            create_datetime=dt.datetime.strftime(
                self.create_datetime, '%Y-%m-%d %H:%M:%S')
        )
        return d

    @staticmethod
    def init_data(commit=True):
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User()
        admin.username = 'admin'
        admin.set_password('admin')
        db.session.add(admin)
        return commit and db.session.commit()
