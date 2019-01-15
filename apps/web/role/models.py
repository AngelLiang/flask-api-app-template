# coding=utf-8

# import os
# import datetime as dt
from enum import Enum, unique

from apps.web.extensions import db

Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime


@unique
class RoleEnum(Enum):
    Administrator = 1
    User = 2


class RolesUsers(Model):
    """角色和帐户关联表"""
    __tablename__ = 'roles_users'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.role_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))


class Role(Model):
    """角色"""
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    users = relationship('User', secondary='roles_users', backref='roles')

    @property
    def id(self):
        return self.role_id

    @id.setter
    def id(self, value):
        self.role_id = value

    def to_dict(self):
        d = dict(id=self.id, name=self.name)
        return d

    @staticmethod
    def init_data(commit=True):
        for role_enum in RoleEnum:
            role = Role.query.get(role_enum.value)
            if role:
                continue
            role = Role()
            role.role_id = role_enum.value
            role.name = role_enum.name
            db.session.add(role)
        return commit and db.session.commit()
