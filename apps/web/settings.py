# coding=utf-8

import os
import sys

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

    # swagger
    SWAGGER = {
        'title': 'Flask-API-APP-TEMPLATE',
        # 'uiversion': 3
    }


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        prefix + os.path.join(BASEDIR, "data-dev.db")
    )
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/flask-app'
    # SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    TESTING = True
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
