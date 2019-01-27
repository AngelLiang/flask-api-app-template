# coding=utf-8

from flask import Blueprint
from flask import jsonify, request
from flask.views import MethodView
# from flask import current_app, g

from flasgger.utils import swag_from

from apps.web.extensions import CORS
from apps.web.exceptions import APIException
from apps.web.auth.utils import generate_token
from apps.web.auth.decorator import api_login_required


from apps.web.user.models import User

user_token_bp = Blueprint("user_token_bp", __name__)
CORS(user_token_bp)


class UserTokenAPI(MethodView):

    decorators = []

    @swag_from('docs/post.yml')
    def post(self):
        """
        POST /api/v1/user/token
        """
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
            token = generate_token(user)
            return jsonify({"token": token})
        else:
            raise APIException('用户名和密码错误！')

    @api_login_required
    @swag_from('docs/delete.yml')
    def delete(self):
        """
        DELETE /api/v1/user/token
        """
        return jsonify()


user_token_bp.add_url_rule('/user/token', view_func=UserTokenAPI.as_view('user_token_api'))
