# coding=utf-8

from flask import Blueprint
from flask import jsonify, request
from flask import current_app, g

from flasgger.utils import swag_from

from apps.web.exceptions import APIException
from apps.web.extensions import CORS, server
from apps.web.user.models import User
from apps.web.auth.utils import generate_token

from .decorator import api_login_required


auth_bp = Blueprint("auth_bp", __name__)
CORS(auth_bp)


@auth_bp.route("/auth/login", methods=["POST"])
@swag_from('docs/login.yml')
def login():
    username = request.values.get("username")
    password = request.values.get("password")

    if username is None or password is None:
        requset_json = request.get_json()
        if requset_json:
            username = requset_json.get("username")
            password = requset_json.get("password")

    if username is None or password is None:
        raise APIException()

    user = User.query.filter_by(username=username).first()
    if user and user.validate_password(password):
        return jsonify({'data': {"token": generate_token(user)}})
    raise APIException('用户名和密码错误！')


@auth_bp.route("/auth/logout", methods=["POST"])
@api_login_required
@swag_from('docs/logout.yml')
def logout():
    """前端登出，清除token即可

    已知问题：jwt生成的token暂时无法在后端清除
    """
    # TODO:
    return '', 204


@auth_bp.route('/oauth/authorize', methods=['GET', 'POST'])
@api_login_required
def authorize():
    current_user = g.current_user
    # Login is required since we need to know the current resource owner.
    # It can be done with a redirection to the login page, or a login
    # form on this authorization page.
    if request.method == 'GET':
        grant = server.validate_consent_request(end_user=current_user)
        return jsonify(grant=grant, user=current_user)
    confirmed = request.values['confirm']
    if confirmed:
        # granted by resource owner
        return server.create_authorization_response(current_user)
    # denied by resource owner
    return server.create_authorization_response(None)


@auth_bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return server.create_token_response()


@auth_bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return server.create_revocation_response()
