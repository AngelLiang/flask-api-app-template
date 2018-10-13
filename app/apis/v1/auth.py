# coding=utf-8

from functools import wraps

from flask import g, current_app, request, jsonify

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

# models
from app.models import User
# blueprint
from app.apis.v1 import api_v1_bp
# utils
from app.apis.v1.utils.response_json import JsonResponse
# errors
from app.apis.v1.errors import NotFoundException
from app.apis.v1.errors import TokenErrorException, TokenTimeOutException


def get_token():
    # 首先从header获取token，如果没有则从参数中获取token
    token = request.headers.get("Authorization") or request.values.get("token")
    return token


def generate_token(user, expiration=60*60*8):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = s.dumps({"user_id": user.id}).decode()
    return token


def validate_token(token):
    if token is None:
        raise TokenErrorException()

    try:
        s = Serializer(current_app.config["SECRET_KEY"])
        data = s.loads(token)
    except SignatureExpired:
        raise TokenTimeOutException()
    except BadSignature:
        raise TokenErrorException()

    user = User.query.get(data["user_id"])
    if user is None:
        raise NotFoundException()

    g.current_user = user
    return user


def api_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 因为在CORS交互中的事先请求（Pre-flight Request）会使用OPTIONS方法发送请求，
        # 所以我们只在OPTIONS方法之外的请求中验证令牌。
        if request.method != "OPTIONS":
            token = get_token()
            user = validate_token(token)
            if not user:
                return jsonify(JsonResponse.fail(u"用户未登录！"))
            return func(*args, **kwargs)
    return decorated_function


@api_v1_bp.route("/auth/login", methods=["POST"])
def login():
    username = request.values.get("username") or request.json.get("username")
    password = request.values.get("password") or request.json.get("password")
    if username is None or password is None:
        raise ParameterMissException()

    user = User.query.filter_by(username=username).first()
    if user and user.validate_password(password):
        token = generate_token(user)
        data = {"token": token}
        return jsonify(JsonResponse.success(data=data))
    return jsonify(JsonResponse.fail())


@api_v1_bp.route("/auth/logout", methods=["GET", "POST"])
def logout():
    return jsonify(JsonResponse.success())
