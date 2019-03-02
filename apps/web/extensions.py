# coding=utf-8

from flask import request

from authlib.flask.oauth2 import AuthorizationServer
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_avatars import Avatars
from flasgger import Swagger, LazyString


db = SQLAlchemy()
cors = CORS()
avatars = Avatars()

template = dict(
    host=LazyString(lambda: request.host),
    base_url=LazyString(lambda: request.base_url)
)
swagger = Swagger(template=template)


server = AuthorizationServer()


def init_auth_server(server, app):
    from apps.web.auth.models import query_client, save_token
    server.init_app(app, query_client=query_client, save_token=save_token)

    # register grant
    # from apps.web.auth.grant import AuthorizationCodeGrant, PasswordGrant, RefreshTokenGrant
    # server.register_grant(AuthorizationCodeGrant)
    # server.register_grant(PasswordGrant)
    # server.register_grant(RefreshTokenGrant)

    from apps.web.auth.models import Token
    from authlib.flask.oauth2.sqla import create_revocation_endpoint
    RevocationEndpoint = create_revocation_endpoint(db.session, Token)
    # register it to authorization server
    server.register_endpoint(RevocationEndpoint)
