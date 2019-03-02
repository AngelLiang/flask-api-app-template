# coding=utf-8

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


class Client(Model, OAuth2ClientMixin):
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
    return Client.query.filter_by(client_id=client_id).first()


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
