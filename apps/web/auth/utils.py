# coding=utf-8

from flask import request, current_app, g

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

from apps.web.exceptions import APIException
from apps.web.user.models import User


def get_token():
    """
    首先从 header 获取 token
    如果没有则从 values（query string or form）中获取 token
    最后再从 json body 获取 token

    retType: tuple(token, token_type)
    """
    # 发送请求时需要把认证令牌附加在请求首部的Authorization字段中，并且在令牌前指定令牌类型（即Bearer）
    # Authorization: Bearer <TOKEN>
    try:
        token_type, token = request.headers['Authorization'].split(None, 1)
        return token, token_type
    except (KeyError, ValueError):  # Authorization字段为空或token为空
        pass

    try:
        return request.values['token'], request.values.get("token_type")
    except KeyError:
        pass

    if request.is_json:
        try:
            return request.json['token'], request.json.get("token_type")
        except KeyError:
            pass

    return None, None


def generate_token(user, expiration=60 * 60 * 8):
    """ return token

    :param user: User
    :param expiration: unit is second
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'user_id': user.id
    })
    return token.decode(), 'Bearer'


def validate_token(token):
    if not token:
        raise APIException('Unauthorized!', 401)
    try:
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token)
    except BadSignature:
        raise APIException('Token Error!', 401)
    except SignatureExpired:
        raise APIException('Token Timeout!', 401)
    else:
        user = User.query.get(data["user_id"])  # 使用令牌中的id来查询对应的用户对象
        if user is None:
            raise APIException('Not Found!', 404)
        g.token_data = data    # 将解析后的token dict存储到g
        return user
