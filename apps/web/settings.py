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
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@127.0.0.2:5432/simple-flask'


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(BASEDIR, "data-dev.db")
    # SQLALCHEMY_ECHO = True
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///"  # in-memory database
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@127.0.0.2:5432/test'


class ProductionConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL",
    #     prefix + os.path.join(BASEDIR, "data.db")
    # )
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
