# coding=utf-8

# import os
import json
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
    """用户"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    create_datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    # ### 用户信息 ###
    fullname = Column(String(20), nullable=False, default='')
    email = Column(String(128), nullable=False, default='', index=True)
    phone = Column(String(20), nullable=False, default='')

    # 存储json格式的额外信息
    additional_info = Column(db.Text(), nullable=False, default='')

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

    def set_additional_info(self, value: str):
        """验证传入的json value并写入数据库additional_info的字段"""
        v = json.loads(value)
        self.additional_info = v

    def get_additional_info(self) -> dict:
        """从数据库加载additional_info字段，返回dict"""
        v = json.dumps(self.additional_info)
        return v

    def to_dict(self):
        d = dict(
            id=self.user_id,
            username=self.username,
            create_datetime=dt.datetime.strftime(self.create_datetime, '%Y-%m-%d %H:%M:%S'),
            fullname=self.fullname,
            phone=self.phone
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
