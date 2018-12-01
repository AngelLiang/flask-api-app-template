# coding=utf-8

from flask import Blueprint
from flask import jsonify, request
# from flask import current_app, g

from apps.web import exceptions
from apps.web.extensions import CORS
from apps.web.utils import JsonResponse

from apps.web.user.models import User
from apps.web.auth.utils import generate_token

auth_bp = Blueprint("auth_bp", __name__)
CORS(auth_bp)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    username = request.values.get("username")
    password = request.values.get("password")
    if username is None or password is None:
        raise exceptions.ParameterMissException()

    user = User.query.filter_by(username=username).first()
    if user and user.validate_password(password):
        token = generate_token(user)
        return jsonify(JsonResponse.success(data={"token": token}))
    return jsonify(JsonResponse.fail())


from .decorator import api_login_required


@auth_bp.route("/auth/logout", methods=["POST"])
@api_login_required
def logout():
    # TODO
    return jsonify(JsonResponse.success())
