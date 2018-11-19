# coding=utf-8

from functools import wraps

from flask import Blueprint
from flask import g, current_app, request, jsonify
from flask_cors import CORS

from werkzeug.security import check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

# extensions
from app.extensions import es
from app.utils import JsonResponse
from app.exceptions import WebException
from app.user.models import User

auth_bp = Blueprint("auth_bp", __name__)

CORS(auth_bp)


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
        raise WebException.TokenErrorException()

    try:
        s = Serializer(current_app.config["SECRET_KEY"])
        data = s.loads(token)
    except SignatureExpired:
        raise WebException.TokenTimeOutException()
    except BadSignature:
        raise WebException.TokenErrorException()

    user = User.get(data["user_id"])
    if user is None:
        raise WebException.NotFoundException()

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


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    username = request.values.get("username")
    password = request.values.get("password")

    if username is None or password is None:
        raise WebException.ParameterMissException()

    res = es.search(
        index=User.es_index, doc_type=User.doc_type,
        body={"query": {"match": {"username": username}}}
    )
    current_app.logger.debug(res)
    hits = res.get('hits')

    if hits:
        hits = hits['hits']
        if len(hits) > 0:
            user = hits[0]
            password_hash = user['_source'].get('password_hash')
            # current_app.logger.debug(password_hash)

            if user and validate_password(password_hash, password):
                token = generate_token(user)
                data = {"token": token}
                return jsonify(JsonResponse.success(data=data))
    return jsonify(JsonResponse.fail())


@auth_bp.route("/auth/logout", methods=["POST"])
@api_login_required
def logout():
    return jsonify(JsonResponse.success())