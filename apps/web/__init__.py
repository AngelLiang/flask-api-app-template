# coding=utf-8

import os
import click
from pprint import pprint
from flask import Flask
from flasgger import LazyJSONEncoder

from apps.web.extensions import db, swagger
from apps.web.extensions import avatars
from apps.web.extensions import server, init_auth_server
from apps.web.settings import config
from apps.web.errors import register_errors
from apps.web.logging import register_logger, register_queue_logger

from apps.web.permission.models import Permission
from apps.web.role.models import Role
from apps.web.user.models import User


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    # 从settings获取配置信息，加载到app.config里
    app.config.from_object(config[config_name])

    # 注册各种模块
    register_logger(app)
    # register_queue_logger(app)
    register_extensions(app)
    register_apis(app)
    register_shell_context(app)
    register_commands(app)
    register_errors(app)

    # app.logger.info('Create {} Flask App'.format(config_name))
    return app


def register_extensions(app):
    db.init_app(app)
    avatars.init_app(app)

    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)

    init_auth_server(server, app)


def register_apis(app):
    from apps.web.auth.apis import auth_bp
    from apps.web.user_token.user_token_api import user_token_bp
    from apps.web.user.apis import user_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(user_token_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initdata():
        """Initialize the data."""
        db.create_all()

        click.echo('Initializing Permission...')
        Permission.init_data()

        click.echo('Initializing Role...')
        Role.init_data()

        click.echo('Initializing User...')
        admin = User.init_data(username='admin', password='admin', commit=False)
        user = User.init_data(username='user', password='user', commit=False)

        from apps.web.role.literals import ADMINISTRATOR, USER
        admin.add_role(ADMINISTRATOR)
        user.add_role(USER)
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

        click.echo('Done.')

    @app.cli.command()
    def printconfig():
        """print the app config"""
        # click.echo(app.config)
        pprint(app.config)
