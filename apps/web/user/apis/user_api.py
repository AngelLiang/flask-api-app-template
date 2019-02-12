# coding=utf-8
"""
单一用户接口
"""

# from sqlalchemy import func
from flasgger.utils import swag_from

# from flask import current_app
from flask.views import MethodView

from apps.web.extensions import db

from apps.web.exceptions import APIException
from apps.web.utils import RequestDict, ResponseJson

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User
from apps.web.user.utils import user_to_dict

from apps.web.user.apis import user_bp


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
        GET /api/v1/users/<user_id>
        """
        user = self.get_models(user_id)
        data = user_to_dict(user)
        return ResponseJson(data=data)

    @swag_from('../docs/user_api/post.yml')
    def post(self, user_id):
        """
        POST /api/v1/users/<user_id>
        """

        request_dict = RequestDict()
        request_dict.check('username', 'password')

        user = self.get_models(user_id)
        user.username = request_dict['username']
        user.set_password(request_dict['password'])

        db.session.add(user)
        db.session.commit()
        data = user_to_dict(user)
        return ResponseJson(data=data), 201

    @swag_from('../docs/user_api/delete.yml')
    def delete(self, user_id):
        """
        DELETE /api/v1/users/<user_id>
        """
        user = self.get_models(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


user_bp.add_url_rule(
    '/users/<user_id>', view_func=UserAPI.as_view('users_id_api'))
