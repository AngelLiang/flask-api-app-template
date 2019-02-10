# coding=utf-8
"""
单一用户接口
"""

# from sqlalchemy import func
from flasgger.utils import swag_from

# from flask import current_app
from flask import request, jsonify
from flask.views import MethodView

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User

from apps.web.user.apis import user_bp
from apps.web.user.apis.utils import user_to_dict


def get_request_parameter_dict():
    if not request.is_json:
        raise APIException()
    return request.get_json()


class UserAPI(MethodView):
    decorators = [api_login_required]

    def get_models(self, user_id):
        try:
            user = User.query.get(int(user_id))
            if not user:
                raise APIException()
        except ValueError:
            raise APIException()
        return user

    @swag_from('../docs/user_api/get.yml')
    def get(self, user_id):
        """
        GET /api/v1/user/<user_id>
        """
        user = self.get_models(user_id)
        data = user_to_dict(user)
        return jsonify({
            'data': data,
            'self': request.url
        })

    @swag_from('../docs/user_api/post.yml')
    def post(self, user_id):
        """
        POST /api/v1/user/<user_id>
        """
        user = self.get_models(user_id)

        request_dict = get_request_parameter_dict()
        if 'username' in request_dict:
            user.username = request_dict['username']
        if 'password' in request_dict:
            password = request_dict['password']
            if password:
                user.set_password(password)

        db.session.add(user)
        db.session.commit()
        data = user_to_dict(user)
        return jsonify({
            'data': data,
            'self': request.url
        }), 201

    @swag_from('../docs/user_api/delete.yml')
    def delete(self, user_id):
        """
        DELETE /api/v1/user/<user_id>
        """
        user = self.get_models(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(), 204


user_bp.add_url_rule(
    '/users/<user_id>', view_func=UserAPI.as_view('user_api'))
