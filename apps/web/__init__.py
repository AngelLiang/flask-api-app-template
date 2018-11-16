# coding=utf-8

import os

# import click
from flask import Flask

from apps.web.extensions import db
from apps.web.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    # 从settings获取配置信息，加载到app.config里
    app.config.from_object(config[config_name])

    # 注册各种模块
    register_extensions(app)
    register_apis(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_apis(app):
    from apps.web.apis.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_commands(app):
    pass
