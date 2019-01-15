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
class PermissionEnum(Enum):
    Administration = 1


class PermissionsUsers(Model):
    """权限和用户关联表"""
    __tablename__ = 'permissions_users'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.permission_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))


class PermissionsRoles(Model):
    """权限和角色关联表"""
    __tablename__ = 'permissions_roles'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.permission_id'))
    role_id = Column(Integer, ForeignKey('role.role_id'))


class Permission(Model):
    """权限"""
    __tablename__ = 'permission'
    permission_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    roles = relationship(
        'Role', secondary='permissions_roles', backref='permissions')
    users = relationship(
        'User', secondary='permissions_users', backref='permissions')

    @property
    def id(self):
        return self.permission_id

    @id.setter
    def id(self, value):
        self.permission_id = value

    def to_dict(self):
        d = dict(id=self.id, name=self.name)
        return d

    @staticmethod
    def init_data(commit=True):
        for permission_enum in PermissionEnum:
            p = Permission.query.get(permission_enum.value)
            if p:
                continue
            p = Permission()
            p.id = permission_enum.value
            p.name = permission_enum.name
            db.session.add(p)
        return commit and db.session.commit()
