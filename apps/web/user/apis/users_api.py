# coding=utf-8
"""
用户集合接口
"""

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import request
from flask import current_app
from flask.views import MethodView


from apps.web.extensions import db


from apps.web.utils import RequestDict, ResponseJson
from apps.web.utils.apis import gen_links, gen_pagination
from apps.web.utils.apis import sort_list

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User
from apps.web.user.utils import user_to_dict

from apps.web.user.apis import user_bp


class UsersAPI(MethodView):

    decorators = [api_login_required]

    @swag_from('../docs/users_api/get.yml')
    def get(self):
        """
        GET /api/v1/users
        """
        request_dict = request.args
        page = request_dict.get('page')
        per_page = request_dict.get('per_page')

        user_query = User.query

        # 排序
        sort = request_dict.get('sort')   # 排序的column
        order = request_dict.get('order')  # 排序顺序：`asc` or `desc`
        if sort == 'id':
            sort = 'user_id'
        user_query = sort_list(User, user_query, sort, order)

        paginate = user_query.paginate(page, per_page)

        total = db.session.query(func.count('*')).select_from(User).scalar()

        items = [user_to_dict(item) for item in paginate.items]
        # data = paginate2dict(paginate, items, total)
        # current_app.logger.debug(items)
        return ResponseJson(
            data=items,
            links=gen_links(paginate, per_page),
            pagination=gen_pagination(paginate.page, per_page, total)
        )

    @swag_from('../docs/users_api/post.yml')
    def post(self):
        """
        POST /api/v1/users
        """
        request_dict = RequestDict()
        request_dict.check('username', 'password')  # 检查参数

        user = User()
        user.username = request_dict['username']
        user.set_password(request_dict['password'])
        db.session.add(user)
        db.session.commit()

        data = user_to_dict(user)
        return ResponseJson(data=data), 201


user_bp.add_url_rule('/users', view_func=UsersAPI.as_view('users_api'))
