# coding=utf-8

# from flask import current_app
from flask import request, jsonify
from flask.views import MethodView

from sqlalchemy import func

# extensions
from app.extensions import db
# models
from app.models import User
# blueprint
from app.apis.v1 import api_v1_bp
# utils
from app.apis.v1.utils.response_json import JsonResponse
from app.apis.v1.errors import ParameterMissException, NotFoundException


def paginate2dict(paginate):
    return dict(
        items=[item.to_dict() for item in paginate.items],
        items_size=len(paginate.items),
        current_page=paginate.page,  # 当前页数
        total_pages=paginate.pages,  # 总页数
        has_prev=paginate.has_prev,  # 是否有前一页
        has_next=paginate.has_next,  # 是否有下一页
        prev_number=paginate.prev_num,   # 前一页数
        next_number=paginate.next_num,   # 后一页数
    )


class UserAPI(MethodView):
    def get(self):
        '''
        GET /api/v1/user
        '''
        page = request.args.get('page', default=1, type=int)
        number = request.args.get('number', default=10, type=int)

        paginate = User.query.paginate(page, number)

        total = db.session.query(func.count('*')).select_from(User).scalar()

        data = {}
        data['items'] = paginate2dict(paginate)
        data['total'] = total
        return jsonify(JsonResponse.success(data=data))

    def post(self):
        '''
        POST /api/v1/user
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        if username is None or password is None:
            raise ParameterMissException()

        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        return jsonify(JsonResponse.success(data=data))


api_v1_bp.add_url_rule('/user', view_func=UserAPI.as_view('user_api'))


class UserIdAPI(MethodView):
    def get(self, user_id):
        '''
        GET /api/v1/user/<user_id>
        '''
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException()
        data = user.to_dict()
        return jsonify(JsonResponse.success(data=data))

    def post(self, user_id):
        '''
        POST /api/v1/user/<user_id>
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        user = User.query.get(user_id)
        if not user:
            raise NotFoundException()
        if username:
            user.username = username
        if password:
            user.set_password(password)
        db.session.add(user)
        db.session.commit()
        data = user.to_dict()
        return jsonify(JsonResponse.success(data=data))

    def delete(self, user_id):
        '''
        DELETE /api/v1/user/<user_id>
        '''
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException()
        db.session.delete(user)
        db.session.commit()
        return jsonify(JsonResponse.success())


api_v1_bp.add_url_rule('/user/<int:user_id>', view_func=UserIdAPI.as_view('user_id_api'))
