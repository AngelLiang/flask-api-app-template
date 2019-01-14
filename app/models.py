# coding=utf-8

import datetime as dt
from flask_rbac import RoleMixin, UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, rbac


Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime


@rbac.as_user_model
class User(Model, UserMixin):
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
            create_datetime=dt.datetime.strftime(self.create_datetime, '%Y-%m-%d %H:%M:%S')
        )
        return d

    @staticmethod
    def init_data():
        admin = User.query.get(1)
        if not admin:
            admin = User()
        admin.username = 'admin'
        admin.set_password('admin')
        db.session.add(admin)

        db.session.commit()


##############################################################################
# Role

ADMINISTRATOR = 'ADMINISTRATOR'
USER = 'USER'

ALL_ROLES = (
    ADMINISTRATOR, USER
)


class RolesUsers(Model):
    """角色和帐户关联表"""
    __tablename__ = 'roles_users'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.role_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))


# role父类多对多表
roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.role_id'))
)


@rbac.as_role_model
class Role(Model, RoleMixin):
    """角色"""
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    users = relationship(
        'User',
        secondary='roles_users',
        backref=db.backref('roles', lazy='dynamic')
    )
    parents = db.relationship(
        'Role',
        secondary=roles_parents,
        primaryjoin=(role_id == roles_parents.c.role_id),
        secondaryjoin=(role_id == roles_parents.c.parent_id),
        backref=db.backref('children', lazy='dynamic')
    )

    # flask_rbac

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    def add_parent(self, parent):
        # You don't need to add this role to parent's children set,
        # relationship between roles would do this work automatically
        self.parents.append(parent)

    def add_parents(self, *parents):
        for parent in parents:
            self.add_parent(parent)

    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()

    # flask_rbac end

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
        for rolename in ALL_ROLES:
            role = Role.query.filter_by(name=rolename).first()
            if not role:
                role = Role(name=rolename)
                db.session.add(role)
        return commit and db.session.commit()

##############################################################################
# Permission


ADMINISTRATION = 'ADMINISTRATION'

ALL_PERMISSIONS = (
    ADMINISTRATION,
)


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
    permission_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # relationship
    roles = relationship('Role', secondary='permissions_roles', backref='permissions')
    users = relationship('User', secondary='permissions_users', backref='permissions')

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
        for permission_name in ALL_PERMISSIONS:
            p = Permission.query.filter_by(name=permission_name).first()
            if not p:
                p = Permission(name=permission_name)
                db.session.add(p)
        return commit and db.session.commit()
