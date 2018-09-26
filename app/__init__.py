# coding=utf-8

import os

import click
from flask import Flask

from app.extensions import db
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("app")

    # 从settings获取配置信息，加载到app.config里
    app.config.from_object(config[config_name])

    # 注册各种模块
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from app.apis.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
