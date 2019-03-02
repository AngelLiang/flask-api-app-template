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


oauth2_server = AuthorizationServer()
oauth1_server = AuthorizationServer()


def init_oauth1_server(server, app):
    from authlib.flask.oauth1 import AuthorizationServer
    from authlib.flask.oauth1.sqla import create_query_client_func
    from apps.web.auth.models import (
        Oauth1Client, TemporaryCredential, TokenCredential, TimestampNonce
    )

    from authlib.flask.oauth1.sqla import (
        register_nonce_hooks,
        register_temporary_credential_hooks,
        register_token_credential_hooks
    )

    register_nonce_hooks(server, db.session, TimestampNonce)
    register_temporary_credential_hooks(server, db.session, TemporaryCredential)
    register_token_credential_hooks(server, db.session, TokenCredential)

    query_client = create_query_client_func(db.session, Oauth1Client)
    server.init_app(app, query_client=query_client)


def init_oauth2_server(server, app):
    from apps.web.auth.models import query_client, save_token

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

    server.init_app(app, query_client=query_client, save_token=save_token)
