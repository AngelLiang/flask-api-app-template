# coding=utf-8
"""
用户集合接口
"""

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import current_app
from flask import url_for
from flask import request, jsonify
from flask.views import MethodView

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.utils import paginate2dict
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User

from apps.web.user.apis import user_bp
from apps.web.user.apis.utils import user_to_dict, gen_links, gen_pagination
from apps.web.user.apis.utils import sort_list


class UsersAPI(MethodView):

    decorators = [api_login_required]

    @swag_from('../docs/users_api/get.yml')
    def get(self):
        """
        GET /api/v1/user
        """
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('perPage', default=10, type=int)

        user_query = User.query

        # 排序
        sort = request.values.get('sort')   # 排序的column
        if sort == 'id':
            sort = 'user_id'
        order = request.values.get('order')  # 排序顺序：`asc` or `desc`
        user_query = sort_list(User, user_query, sort, order)

        paginate = user_query.paginate(page, per_page)

        total = db.session.query(func.count('*')).select_from(User).scalar()

        items = [user_to_dict(item) for item in paginate.items]
        # data = paginate2dict(paginate, items, total)
        # current_app.logger.debug(items)
        return jsonify({
            'pagination': gen_pagination(paginate.page, per_page, total),
            'links': gen_links(paginate, per_page),
            'data': items,
            'self': request.url
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
            'data': data,
            'self': request.url
        })


user_bp.add_url_rule('/users', view_func=UsersAPI.as_view('users_api'))
