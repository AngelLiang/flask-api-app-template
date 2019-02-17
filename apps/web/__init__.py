# coding=utf-8

import os


import click
from flask import Flask
from flasgger import LazyJSONEncoder

from apps.web.extensions import db, swagger
from apps.web.settings import config

from apps.web.errors import register_errors
from apps.web.logging import register_logger

from apps.web.permission.models import Permission
from apps.web.role.models import Role
from apps.web.user.models import User


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)

    # 从settings获取配置信息，加载到app.config里
    app.config.from_object(config[config_name])

    # 注册各种模块
    register_logger(app)
    register_extensions(app)
    register_apis(app)
    register_shell_context(app)
    register_commands(app)
    register_errors(app)

    app.logger.info('Create Flask App')
    return app


def register_extensions(app):
    db.init_app(app)

    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)


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
        return dict(db=db)


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
        User.init_data()

        from apps.web.role.literals import ADMINISTRATOR
        admin = User.query.filter_by(username='admin').first()
        if admin:
            admin.add_role(ADMINISTRATOR)
            db.session.add(admin)
            db.session.commit()
