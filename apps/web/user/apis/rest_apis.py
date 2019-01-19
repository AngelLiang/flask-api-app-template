# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import current_app
from flask import request, jsonify
from flask.views import MethodView

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.utils import paginate2dict
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User


from .apis import user_bp


class UserAPI(MethodView):

    decorators = [api_login_required]

    @swag_from('../docs/user_api/get.yml')
    def get(self):
        """
        GET /api/v1/user
        """
        page = request.args.get('page', default=1, type=int)
        number = request.args.get('number', default=10, type=int)

        paginate = User.query.paginate(page, number)

        total = db.session.query(func.count('*')).select_from(User).scalar()

        data = paginate2dict(paginate)
        data['total'] = total
        current_app.logger.debug(data)
        return jsonify(data)

    @swag_from('../docs/user_api/post.yml')
    def post(self):
        """
        POST /api/v1/user
        """
        request_json = request.get_json()
        if not request_json:
            raise APIException()

        username = request_json.get('username')
        password = request_json.get('password')

        if username is None or password is None:
            raise APIException()

        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        return jsonify(data)


user_bp.add_url_rule('/user', view_func=UserAPI.as_view('user_api'))


class UserIdAPI(MethodView):
    decorators = [api_login_required]

    @swag_from('../docs/user_id_api/get.yml')
    def get(self, user_id):
        """
        GET /api/v1/user/<user_id>
        """
        user = User.query.get(user_id)
        if not user:
            raise APIException()
        data = user.to_dict()
        return jsonify(data)

    @swag_from('../docs/user_id_api/post.yml')
    def post(self, user_id):
        """
        POST /api/v1/user/<user_id>
        """
        request_json = request.get_json()
        if not request_json:
            raise APIException()

        user = User.query.get(user_id)
        if not user:
            raise APIException()

        username = request_json.get('username')
        password = request_json.get('password')

        if username:
            user.username = username
        if password:
            user.set_password(password)

        db.session.add(user)
        db.session.commit()
        data = user.to_dict()
        return jsonify(data)

    @swag_from('../docs/user_id_api/delete.yml')
    def delete(self, user_id):
        """
        DELETE /api/v1/user/<user_id>
        """
        user = User.query.get(user_id)
        if not user:
            raise APIException()
        db.session.delete(user)
        db.session.commit()
        return jsonify()


user_bp.add_url_rule(
    '/user/<user_id>', view_func=UserIdAPI.as_view('user_id_api'))
