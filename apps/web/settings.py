# coding=utf-8

import os
import sys

# BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASEDIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

# SQLite URI compatible
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "secret string"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ### MAIL ###
    MAIL_DEBUG = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', default=587))
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', default=False)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=False)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # 默认发信人由一个两元素元组组成，即（姓名，邮箱地址）
    MAIL_DEFAULT_SENDER = ('flask-api-app-template', os.getenv('MAIL_USERNAME', default='noreply@example.com'))


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(BASEDIR, "data-dev.db")
    # REDIS_URL = "redis://localhost"
    # SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        prefix + os.path.join(BASEDIR, "data.db")
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
