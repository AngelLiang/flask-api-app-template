# coding=utf-8

# from flask import current_app
from flask import request, jsonify
from flask.views import MethodView

from sqlalchemy import func

from app.extensions import db
from app.exceptions import APIException
from app.utils import JsonResponse, paginate2dict
from app.models import User
from app.apis.v1 import api_v1_bp
from app.apis.v1.auth import api_login_required


@api_v1_bp.route("/user/total", methods=["GET"])
@api_login_required
def user_total():
    total = db.session.query(func.count('*')).select_from(User).scalar()
    data = {'total': total}
    return jsonify(JsonResponse.success(data=data))


class UserAPI(MethodView):
    decorators = [api_login_required]

    def get(self):
        '''
        GET /api/v1/user
        '''
        page = request.args.get('page', default=1, type=int)
        number = request.args.get('number', default=10, type=int)

        paginate = User.query.paginate(page, number)

        total = db.session.query(func.count('*')).select_from(User).scalar()

        data = paginate2dict(paginate)
        data['total'] = total
        return jsonify(JsonResponse.success(data=data))

    def post(self):
        '''
        POST /api/v1/user
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        if username is None or password is None:
            raise APIException()

        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        return jsonify(JsonResponse.success(data=data))


api_v1_bp.add_url_rule('/user', view_func=UserAPI.as_view('user_api'))


class UserIdAPI(MethodView):
    decorators = [api_login_required]

    def get(self, user_id):
        '''
        GET /api/v1/user/<user_id>
        '''
        user = User.query.get(user_id)
        if not user:
            raise APIException()
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
            raise APIException()
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
            raise APIException()
        db.session.delete(user)
        db.session.commit()
        return jsonify(JsonResponse.success())


api_v1_bp.add_url_rule('/user/<user_id>', view_func=UserIdAPI.as_view('user_id_api'))
