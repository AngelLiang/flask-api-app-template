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

from .literals import ALL_PERMISSIONS


class PermissionsUsers(Model):
    """权限和帐户关联表"""
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
    id = Column('permission_id', Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    roles = relationship(
        'Role', secondary='permissions_roles', backref='permissions')
    users = relationship(
        'User', secondary='permissions_users', backref='permissions')

    def to_dict(self):
        d = dict(id=self.id, name=self.name)
        return d

    @staticmethod
    def init_data(commit=True):
        for i, permission_name in enumerate(ALL_PERMISSIONS, start=1):
            permission = Permission.query.get(i)
            if permission is None:
                permission = Permission()
            permission.name = permission_name
            db.session.add(permission)
        return commit and db.session.commit()
