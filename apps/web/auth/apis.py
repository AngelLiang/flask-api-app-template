# coding=utf-8

from flask import Blueprint
from flask import jsonify, request, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

# from app.extensions import db
# models
from apps.web.user.models import User

from apps.web.utils import JsonResponse
# errors
from apps.web.errors import ParameterMissException, NotFoundException
from apps.web.errors import TokenTimeOutException, TokenErrorException


auth_bp = Blueprint("auth_bp", __name__)


def get_token():
    # 首先从header获取token，如果没有则从参数中获取token
    token = request.headers.get("Authorization") or request.values.get("token")
    return token


def generate_token(user, expiration=60 * 60 * 8):
    """生成token
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = s.dumps({"user_id": user.id})
    return token.decode()


def validate_token(token):
    if not token:
        return None
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise TokenErrorException()
        # return False
    except SignatureExpired:
        raise TokenTimeOutException()
        # return False
    user = User.query.get(data["user_id"])  # 使用令牌中的id来查询对应的用户对象
    if user is None:
        raise NotFoundException("没有该用户！")
        # return False
    g.current_user = user  # 将用户对象存储到g上
    return user


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    username = request.values.get("username")
    password = request.values.get("password")
    if username is None or password is None:
        raise ParameterMissException()

    user = User.query.filter_by(username=username).first()
    if user and user.validate_password(password):
        token = generate_token(user)
        return jsonify(JsonResponse.success(data={"token": token}))
    return jsonify(JsonResponse.fail())


from .decorator import api_login_required


@auth_bp.route("/auth/logout", methods=["POST"])
@api_login_required
def logout():
    return jsonify(JsonResponse.success())
