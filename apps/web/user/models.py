# coding=utf-8

# import os
import datetime as dt

from werkzeug.security import generate_password_hash, check_password_hash

from apps.web.extensions import db
from apps.web.utils import JsonType


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
    id = Column('user_id', Integer, primary_key=True)
    # ### 帐号基本字段 ###
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)

    # ### 帐号状态信息 ###

    # 帐号启用状态，创建帐号时为False
    # 可以管理员手动激活，或者发送confirm-email时激活
    # 管理员可以标识此字段禁用用户
    is_active = Column(Boolean, nullable=False, default=False)
    state = Column(String(10), nullable=False, default='')
    # 创建时间
    create_datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    # ### 用户信息 ###
    fullname = Column(String(20), nullable=False, default='')
    # 邮箱
    email = Column(String(255), nullable=False, default='')
    # 邮件确认标志
    # 当用户点击confirm-emil中的链接后，表示确认用户使用该邮箱
    is_email_confirm = Column(Boolean, nullable=False, default=False)
    # 手机号码
    phone = Column(String(20), nullable=False, default='')
    # 手机号码确认标识
    is_phone_confirm = Column(Boolean, nullable=False, default=False)

    # 存储json格式的额外信息
    # additional_info = Column(db.Text(), nullable=False, default='{}')
    # additional_info = Column(JSON, nullable=False, default={})
    additional_info = Column(JsonType)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def set_additional_info(self, value: dict):
    #     """验证传入的json value并写入数据库additional_info的字段"""
    #     v = json.dumps(value)
    #     self.additional_info = v

    # def get_additional_info(self) -> dict:
    #     """从数据库加载additional_info字段，返回dict"""
    #     v = json.loads(self.additional_info)
    #     return v

    def to_dict(self):
        d = dict(
            id=self.id,
            username=self.username,

            is_active=self.is_active,
            create_datetime=dt.datetime.strftime(
                self.create_datetime, '%Y-%m-%d %H:%M:%S'),

            fullname=self.fullname,
            email=self.email,
            is_email_confirm=self.is_email_confirm,
            phone=self.phone,
            is_phone_confirm=self.is_phone_confirm
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
