# coding=utf-8

from flask import current_app, request, jsonify
from flask.views import MethodView

# extensions
from app.extensions import es
# models
from app.models import User
# blueprint
from app.apis.v1 import api_v1_bp
# utils
from app.apis.v1.utils.response_json import JsonResponse
from app.apis.v1.errors import ParameterMissException


class UserAPI(MethodView):
    def get(self):
        '''
        GET /api/v1/user
        '''
        # page = request.args.get('page', default=1, type=int)
        # number = request.args.get('number', default=10, type=int)

        res = es.search(
            index="user-index", doc_type='user',
            body={'query': {'match_all': {}}}
        )
        current_app.logger.debug(res)

        hits = res['hits']
        total = hits['total']
        items = hits['hits']

        data = {}
        data['total'] = total
        data['items'] = items
        data['items_size'] = len(items)
        return jsonify(JsonResponse.success(data=data))

    def post(self):
        '''
        POST /api/v1/user
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        if username is None or password is None:
            raise ParameterMissException()

        data = User.create(username, password)
        return jsonify(JsonResponse.success(data=data))


api_v1_bp.add_url_rule('/user', view_func=UserAPI.as_view('user-api'))


class UserIdAPI(MethodView):
    def get(self, user_id):
        '''
        GET /api/v1/user/<user_id>
        '''
        res = es.get(index="user-index", doc_type='user', id=user_id)
        current_app.logger.debug(res)
        data = res
        return jsonify(JsonResponse.success(data=data))

    def post(self, user_id):
        '''
        POST /api/v1/user/<user_id>
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        data = User.update(user_id, username, password)
        return jsonify(JsonResponse.success(data=data))

    def delete(self, user_id):
        '''
        DELETE /api/v1/user/<user_id>
        '''
        pass


api_v1_bp.add_url_rule('/user/<any:user_id>', view_func=UserIdAPI.as_view('user_id-api'))
