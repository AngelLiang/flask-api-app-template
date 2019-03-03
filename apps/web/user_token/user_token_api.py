# coding=utf-8

from flask import Blueprint
from flask import jsonify, request
from flask import current_app, g
from flask.views import MethodView

from webargs.flaskparser import parser
from webargs import fields, validate
from flasgger.utils import swag_from

from apps.web.extensions import CORS
from apps.web.exceptions import APIException
from apps.web.utils import RequestDict, ResponseJson
from apps.web.auth.utils import generate_token
from apps.web.auth.decorator import api_login_required


from apps.web.user.models import User

user_token_bp = Blueprint("user_token_bp", __name__)
CORS(user_token_bp)


token_args = {
    "username": fields.Str(required=True),
    "password": fields.Str(required=True)
}


class UserTokenAPI(MethodView):

    decorators = []

    @swag_from('docs/post.yml')
    def post(self):
        """
        POST /api/v1/users/token
        """
        request_dict = RequestDict()

        # check
        # username, password = request_dict.check('username', 'password')
        args = parser.parse(token_args, request)
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            expiration = request_dict.get('expiration', default=60 * 60 * 8)
            token, token_type = generate_token(user, expiration)
            data = dict(token=token, type=token_type, expiration=expiration)
            links = {}
            response = ResponseJson(data=data, links=links)
            # 当返回的响应中包含令牌等敏感信息时，我们应该将
            # 响应首部Cache-Control字段的值设为no-store，
            # 将Pramga字段的值设为no-cache。
            response.headers['Cache-Control'] = 'no-store'
            response.headers['Pragma'] = 'no-cache'
            return response, 201
        else:
            raise APIException('用户名和密码错误！')

    @api_login_required
    @swag_from('docs/delete.yml')
    def delete(self):
        """
        DELETE /api/v1/users/token
        """
        return '', 204


view_func = UserTokenAPI.as_view('user_token_api')
user_token_bp.add_url_rule('/users/token', view_func=view_func)
