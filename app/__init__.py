# coding=utf-8

import os

import click
from flask import Flask

from app.extensions import es
from app.user.models import User
from app.settings import config

from .errors import register_errors


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)

    # 从settings获取配置信息，加载到app.config里
    app.config.from_object(config[config_name])

    # 注册各种模块
    register_extensions(app)
    register_apis(app)
    register_shell_context(app)
    register_commands(app)
    register_errors(app)

    return app


def register_extensions(app):
    pass


def register_apis(app):
    from app.auth.apis import auth_bp
    from app.user.apis import user_bp
    url_prefix = '/api/v1'
    app.register_blueprint(auth_bp, url_prefix=url_prefix)
    app.register_blueprint(user_bp, url_prefix=url_prefix)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(es=es, User=User)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            # db.drop_all()
            click.echo('Drop tables.')
        # db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initdata():
        """Initialize data."""
        click.echo('Initializing the database...')

        click.echo('Initializing User...')
        User.init_data()
