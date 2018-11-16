# coding=utf-8

# import os
from enum import Enum, unique
import datetime as dt

# from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime


class Account(Model):
    '''帐户'''
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    create_datetime = Column(DateTime, nullable=False, default=dt.datetime.now)

    @property
    def id(self):
        return self.account_id

    @id.setter
    def id(self, value):
        self.account_id = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        d = dict(
            id=self.account_id,
            username=self.username,
            create_datetime=dt.datetime.strftime(self.create_datetime, '%Y-%m-%d %H:%M:%S')
        )
        return d

    @staticmethod
    def init_data():
        admin = Account.query.get(1)
        if not admin:
            admin = Account()
        admin.username = 'admin'
        admin.set_password('admin')
        db.session.add(admin)

        db.session.commit()

##############################################################################
# Role


@unique
class RoleEnum(Enum):
    Administrator = 1
    User = 2


class RolesAccounts(Model):
    '''角色和帐户关联表'''
    __tablename__ = 'roles_accounts'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.role_id'))
    account_id = Column(Integer, ForeignKey('account.account_id'))


class Role(Model):
    '''角色'''
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    accounts = relationship('Account', secondary='roles_accounts', backref='roles')

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
    def init_data():
        for role_enum in RoleEnum:
            role = Role.query.get(role_enum.value)
            if not role:
                role = Role()
            role.role_id = role_enum.value
            role.name = role_enum.name
            db.session.add(role)
        db.session.commit()

##############################################################################
# Permission


@unique
class PermissionEnum(Enum):
    Administration = 1


class PermissionsAccounts(Model):
    '''权限和帐户关联表'''
    __tablename__ = 'permissions_accounts'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.permission_id'))
    account_id = Column(Integer, ForeignKey('account.account_id'))


class PermissionsRoles(Model):
    '''权限和角色关联表'''
    __tablename__ = 'permissions_roles'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.permission_id'))
    role_id = Column(Integer, ForeignKey('role.role_id'))


class Permission(Model):
    '''权限'''
    __tablename__ = 'permission'
    permission_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    roles = relationship('Role', secondary='permissions_roles', backref='permissions')
    accounts = relationship('Account', secondary='permissions_accounts', backref='permissions')

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
    def init_data():
        for permission_enum in PermissionEnum:
            p = Permission.query.get(permission_enum.value)
            if not p:
                p = Permission()
            p.id = permission_enum.value
            p.name = permission_enum.name
            db.session.add(p)
        db.session.commit()
