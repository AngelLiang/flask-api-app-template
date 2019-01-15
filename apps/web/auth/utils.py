# coding=utf-8

from flask import request, current_app, g

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

from apps.web import exceptions
from apps.web.user.models import User


def get_token():
    """获取token"""
    # 首先从header获取token，如果没有则从参数中获取token
    token = request.headers.get("Authorization") or request.values.get("token")
    return token


def generate_token(user, expiration=60 * 60 * 8):
    """生成token"""
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = s.dumps({"user_id": user.id})
    return token.decode()


def validate_token(token):
    """验证token"""
    if not token:
        return None
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise exceptions.TokenErrorException()
        # return False
    except SignatureExpired:
        raise exceptions.TokenTimeOutException()
        # return False
    user = User.query.get(data["user_id"])  # 使用令牌中的id来查询对应的用户对象
    if user is None:
        raise exceptions.NotFoundException("没有该用户！")
        # return False
    g.current_user = user  # 将用户对象存储到g上
    return user
