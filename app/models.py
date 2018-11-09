# coding=utf-8

# import os
# import datetime as dt

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


class User(Model):
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128))

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
            username=self.username
        )
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

##############################################################################
# Role


RoleAndUser = db.Table(
    'role_and_user',
    Column('role_id', Integer, db.ForeignKey('role.role_id')),
    Column('user_id', Integer, db.ForeignKey('user.user_id'))
)


class Role(Model):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    permissions = relationship('Permission', secondary='permission_and_role', back_populates='roles')
    users = relationship('User', secondary='role_and_user')

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
        role_list = ['Administrator', 'User']
        for item in role_list:
            role = Role()
            role.name = item
            db.session.add(role)
        db.session.commit()

##############################################################################
# Permission


# relationship table
PermissionAndUser = db.Table(
    'permission_and_user',
    Column('permission_id', Integer, db.ForeignKey('permission.permission_id')),
    Column('user_id', Integer, db.ForeignKey('user.user_id')),
)

PermissionAndRole = db.Table(
    'permission_and_role',
    Column('permission_id', Integer, db.ForeignKey('permission.permission_id')),
    Column('role_id', Integer, db.ForeignKey('role.role_id'))

)


class Permission(Model):
    __tablename__ = 'permission'
    permission_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    roles = relationship('Role', secondary='permission_and_role', back_populates='permissions')
    # users = relationship('User', secondary='permission_and_user', back_populates='permissions')

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
        pass
