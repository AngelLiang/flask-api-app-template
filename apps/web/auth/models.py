# coding=utf-8

from authlib.flask.oauth1.sqla import (
    OAuth1ClientMixin, OAuth1TemporaryCredentialMixin, OAuth1TokenCredentialMixin
)
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin
)


from apps.web.extensions import db


Model = db.Model
ForeignKey = db.ForeignKey
relationship = db.relationship

Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime
Text = db.Text


class Oauth1Client(Model, OAuth1ClientMixin):
    __tablename__ = 'oauth1_client'
    id = Column(db.Integer, primary_key=True)
    user_id = Column(
        Integer, db.ForeignKey('user.user_id', ondelete='CASCADE')
    )
    user = relationship('User')


class TemporaryCredential(Model, OAuth1TemporaryCredentialMixin):
    """
    A temporary credential is used to exchange a token credential.
    It is also known as “request token and secret”. Since it is
    temporary, it is better to save them into cache instead of database.
    """
    __tablename__ = 'temporary_credential'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    user = relationship('User')


class TokenCredential(Model, OAuth1TokenCredentialMixin):
    """
    A token credential is used to access resource owners’ resources.
    Unlike OAuth 2, the token credential will not expire in OAuth 1.
    This token credentials are supposed to be saved into a persist
    database rather than a cache.
    """
    __tablename__ = 'token_credential'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    user = relationship('User')

    def set_user_id(self, user_id):
        self.user_id = user_id


class TimestampNonce(db.Model, OAuth1TokenCredentialMixin):
    """
    The nonce value MUST be unique across all requests with the same
    timestamp, client credentials, and token combinations. Authlib
    Flask integration has a built-in validation with cache.

    If cache is not available, there is also a SQLAlchemy mixin:
    """
    __tablename__ = 'timestamp_nonce'
    id = db.Column(Integer, primary_key=True)


class Oauth2Client(Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    user = relationship('User')


class OAuth2AuthorizationCode(Model, OAuth2AuthorizationCodeMixin):
    """

    Authorization Code Grant is a very common grant type, it is supported by
    almost every OAuth 2 providers. It uses an authorization code to exchange
    access token. In this case, we need a place to store the authorization code.
    It can be kept in a database or a cache like redis.

    https://docs.authlib.org/en/latest/flask/2/grants.html
    """
    __tablename__ = 'oauth2_code'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    user = relationship('User')


class Token(Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))

    user = relationship('User')


def query_client(client_id):
    return Oauth2Client.query.filter_by(client_id=client_id).first()


def save_token(token, request):
    if request.current_user:
        user_id = request.current_user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        user_id = None
    item = Token(
        client_id=request.client.client_id,
        user_id=user_id,
        **token
    )
    db.session.add(item)
    db.session.commit()
