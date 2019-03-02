# coding=utf-8

from authlib.specs.rfc6749 import grants
from authlib.common.security import generate_token

from apps.web.extensions import db

from apps.web.user.models import User
from apps.web.auth.models import OAuth2AuthorizationCode, Token


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user, request):
        # you can use other method to generate this code
        code = generate_token(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.get_user_id(),
        )
        db.session.add(item)
        db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        item = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    """
    Resource owner uses his username and password to exchange an
    access token, this grant type should be used only when the
    client is trustworthy, implement it with a subclass of
    ResourceOwnerPasswordCredentialsGrant
    """

    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user.validate_password(password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    """
    Many OAuth 2 providers haven’t implemented refresh token
    endpoint. Authlib provides it as a grant type, implement it
    with a subclass of RefreshTokenGrant
    """

    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_refresh_token(self, refresh_token):
        item = Token.query.filter_by(refresh_token=refresh_token).first()
        # define is_refresh_token_expired by yourself
        if item and not item.is_refresh_token_expired():
            return item

    def authenticate_user(self, credential):
        return User.query.get(credential.user_id)
