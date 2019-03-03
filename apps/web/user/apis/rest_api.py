# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from
from flask import current_app
from flask.views import MethodView

from apps.web.extensions import db
from apps.web.exceptions import APIException
from apps.web.utils import RequestDict, ResponseJson
from apps.web.utils import gen_links, gen_pagination, sort_list
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User, user_to_dict
from apps.web.user.apis import user_bp


class UsersAPI(MethodView):
    decorators = [api_login_required]

    @swag_from('../docs/rest_api/get.yml', endpoint='user_bp.users_api')
    @swag_from('../docs/rest_api/get_with_id.yml', endpoint='user_bp.users_api_with_id')
    def get(self, user_id=None):
        """
        GET /api/v1/users
        GET /api/v1/users/<user_id>
        """
        if user_id is None:
            # return a list of users
            request_dict = RequestDict()

            user_query = User.query

            # 排序：默认按id升序排序
            sort = request_dict.get('sort', default='id')   # 排序的column
            # 排序顺序：`asc` or `desc`
            order = request_dict.get('order', default='asc')
            if sort == 'id':
                sort = 'user_id'
            user_query = sort_list(User, user_query, sort, order)

            # 分页
            page = request_dict.get_page()
            per_page = request_dict.get_per_page()
            paginate = user_query.paginate(page, per_page)
            total = db.session.query(func.count('*')).select_from(User).scalar()

            include = request_dict.get_include()
            exclude = request_dict.get_exclude()
            items = [user_to_dict(item, include=include, exclude=exclude) for item in paginate.items]
            return ResponseJson(
                data=items,
                links=gen_links(paginate, per_page),
                pagination=gen_pagination(paginate.page, per_page, total)
            )
        else:
            # expose a single user
            user = User.get_by_id(user_id)
            request_dict = RequestDict()
            include = request_dict.get_include()
            exclude = request_dict.get_exclude()
            data = user_to_dict(user, include=include, exclude=exclude)
            return ResponseJson(data=data)

    @swag_from('../docs/rest_api/post.yml')
    def post(self):
        """
        POST /api/v1/users
        """
        request_dict = RequestDict()
        # check
        username, password = request_dict.check('username', 'password')

        if User.is_username_exist(username):
            raise APIException('用户名已经存在！')

        # creata
        user = User()
        # update
        user.username = username
        user.set_password(password)
        rolename = request_dict.get('rolename')
        if rolename:
            user.add_role(rolename, commit=False)
        input_json = request_dict.get_json(to_uncamelize=True)
        user.update(**input_json, attrs=('fullname', 'description',), commit=False)
        # commit
        db.session.add(user)
        db.session.commit()

        include = request_dict.get_include()
        exclude = request_dict.get_exclude()
        data = user_to_dict(user, include=include, exclude=exclude)
        return ResponseJson(data=data), 201

    @swag_from('../docs/rest_api/put.yml')
    def put(self, user_id):
        """
        PUT /api/v1/users/<user_id>
        """
        request_dict = RequestDict()

        user = User.get_by_id(user_id)
        # update & commit
        input_json = request_dict.get_json(to_uncamelize=True)
        user.update(**input_json, attrs=('fullname', 'description',), commit=True)

        include = request_dict.get_include()
        exclude = request_dict.get_exclude()
        data = user_to_dict(user, include=include, exclude=exclude)
        return ResponseJson(data=data)

    @swag_from('../docs/rest_api/delete.yml')
    def delete(self, user_id):
        """
        DELETE /api/v1/users/<user_id>
        """
        user = User.get_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


view_func = UsersAPI.as_view('users_api')
# user_bp.add_url_rule('/users', defaults={'user_id': None}, methods=['GET'], view_func=view_func)
user_bp.add_url_rule('/users', methods=['GET', 'POST'], view_func=view_func)
user_bp.add_url_rule('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'],
                     endpoint='users_with_id_api', view_func=view_func)
