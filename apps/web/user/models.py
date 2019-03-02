# coding=utf-8

import os
import datetime as dt

from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_avatars import Identicon

from apps.web.extensions import db, avatars
from apps.web.utils import JsonType, datetime_format
from apps.web.utils import camelize_for_dict_key, exclude_dict_key
from apps.web.mixin import ModelMixin


Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime
Text = db.Text


class User(Model, ModelMixin):
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
    # 描述
    description = Column(Text(), nullable=False, default='')

    # 存储json格式的额外信息
    # additional_info = Column(db.Text(), nullable=False, default='{}')
    # additional_info = Column(JSON, nullable=False, default={})
    additional_info = Column(JsonType)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_user_id(self):
        """for authlib"""
        return self.id

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

    #################################################################
    # Role
    #################################################################

    def add_role(self, rolename, commit=True):
        """add role to user

        :param rolename: 角色名称
        """
        from apps.web.role.models import Role
        role = Role.query.filter_by(name=rolename).first()
        if role:
            self.roles.append(role)
            db.session.add(self)
            return commit and db.session.commit()

    def is_administrator(self):
        from apps.web.role.literals import ADMINISTRATOR
        return ADMINISTRATOR in [role.name for role in self.roles]

    @classmethod
    def is_username_exist(cls, username):
        # user = User.query.filter(exists().where(User.username == username)).first()
        return User.query.filter(User.username == username).first()

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first_or_404()

    def update(self, password=None, commit=True, **kw):
        if password is not None:
            self.set_password(password)
        return ModelMixin.update(self, commit=commit, **kw)

    def generate_avatar(self):
        """unused"""
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    def to_dict(self, include: list = None, exclude: list = None, to_camelize=True):
        data = dict(
            id=self.id,
            username=self.username,

            is_active=self.is_active,
            create_datetime=datetime_format(self.create_datetime),

            fullname=self.fullname,
            email=self.email,
            is_email_confirm=self.is_email_confirm,
            phone=self.phone,
            is_phone_confirm=self.is_phone_confirm,
            description=self.description,
            # avatar
            avatar=avatars.default(),
            avatar_s=avatars.default(size='s'),
            avatar_l=avatars.default(size='l')
        )
        if include:
            if 'roles' in include:
                data['roles'] = [role.name for role in self.roles]
        if exclude:
            data = exclude_dict_key(data, exclude)
        if to_camelize:
            data = camelize_for_dict_key(data)
        return data

    @staticmethod
    def init_data(username='admin', password='admin', commit=True):
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        return commit and db.session.commit() or user


def user_to_dict(user: User, include: list = None, exclude: list = None, to_camelize=True):
    data = user.to_dict(include=include, exclude=exclude, to_camelize=to_camelize)

    # add links
    links = dict()
    if not user.is_administrator():
        links['changeUserActive'] = url_for('user_bp.user_is_active', user_id=user.id, _external=True)
    data['links'] = links

    if include:
        pass
    if exclude:
        data = exclude_dict_key(data, exclude)
    if to_camelize:
        data = camelize_for_dict_key(data)
    return data
