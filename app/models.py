# coding=utf-8

import os
import datetime as dt

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


Model = db.Model
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String


class User(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
