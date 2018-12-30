# coding=utf-8

from flask import g, current_app

from flask_sqlalchemy import SQLAlchemy
from flask_rbac import RBAC

db = SQLAlchemy()
rbac = RBAC()


def get_current_user():
    with current_app.request_context():
        return g.current_user


rbac.set_user_loader(get_current_user)
