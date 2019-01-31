# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import current_app, url_for
from flask import request, jsonify
from flask.views import MethodView

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.utils import paginate2dict
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User

from apps.web.user.apis import user_bp
from apps.web.user.apis.utils import user_to_dict


class UsersAPI(MethodView):

    decorators = [api_login_required]

    @swag_from('../docs/users_api/get.yml')
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
        return jsonify({
            'data': data,
        })

    @swag_from('../docs/users_api/post.yml')
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

        data = user_to_dict(user)
        return jsonify({
            'data': data
        })


user_bp.add_url_rule('/users', view_func=UsersAPI.as_view('users_api'))
