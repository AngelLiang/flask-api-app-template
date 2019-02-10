# coding=utf-8

from flask import request, current_app, g

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

from apps.web.exceptions import APIException
from apps.web.user.models import User


def get_token():
    """获取token"""
    # 首先从 header 获取 token
    # 如果没有则从 values（query string or form）中获取 token
    # 最后再从 json body 获取 token
    try:
        # Authorization: token <TOKEN>
        token = None
        Authorization = request.headers.get("Authorization")
        if Authorization:
            token_type, token = Authorization.split(None, 1)
            if token_type and token_type.upper() == 'TOKEN':
                return token
    except ValueError:  # Authorization字段为空或token为空
        token = None
    if not token:
        token = request.values.get("token")
    if not token:
        request_json = request.get_json()
        if request_json:
            token = request_json.get("token")
    return token


def generate_token(user, expiration=60 * 60 * 8):
    """生成token"""
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = s.dumps({"user_id": user.id})
    return token.decode()


def validate_token(token):
    """验证token"""
    if not token:
        raise APIException('未认证！', 403)
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise APIException('Token错误！', 403)
    except SignatureExpired:
        raise APIException('Token超时！', 403)
    user = User.query.get(data["user_id"])  # 使用令牌中的id来查询对应的用户对象
    if user is None:
        raise APIException('没有该用户！', 404)
    g.current_user = user  # 将用户对象存储到g上
    return user
