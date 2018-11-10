# coding=utf-8

from functools import wraps

from flask import g, current_app, request, jsonify

from werkzeug.security import check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

# extensions
from app.extensions import es
# models
from app.models import User
# blueprint
from app.apis.v1 import api_v1_bp
# utils
from app.apis.v1.utils.response_json import JsonResponse
# errors
from app.apis.v1.errors import NotFoundException
from app.apis.v1.errors import TokenErrorException, TokenTimeOutException
from app.apis.v1.errors import ParameterMissException


def get_token():
    # 首先从header获取token，如果没有则从参数中获取token
    token = request.headers.get("Authorization") or request.values.get("token")
    return token


def generate_token(user, expiration=60 * 60 * 8):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = s.dumps({"user_id": user['_id']}).decode()
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

    user = User.get(data["user_id"])
    if user is None:
        raise NotFoundException()

    g.current_user = user
    return user


def validate_password(password_hash, password):
    return check_password_hash(password_hash, password)


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
    username = request.values.get("username")
    password = request.values.get("password")

    if username is None or password is None:
        raise ParameterMissException()

    res = es.search(
        index="user-index", doc_type='user',
        body={"query": {"match": {"username": username}}}
    )
    current_app.logger.debug(res)
    hits = res['hits']['hits']
    if len(hits) > 0:
        user = hits[0]
        password_hash = user['_source']['password_hash']
        current_app.logger.debug(password_hash)

        if user and validate_password(password_hash, password):
            token = generate_token(user)
            data = {"token": token}
            return jsonify(JsonResponse.success(data=data))
    return jsonify(JsonResponse.fail())


@api_v1_bp.route("/auth/logout", methods=["POST"])
@api_login_required
def logout():
    return jsonify(JsonResponse.success())
