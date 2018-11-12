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
from app.apis.v1.errors import ParameterMissException, ParameterErrorException


class UserAPI(MethodView):
    def get(self):
        '''
        GET /api/v1/user
        '''
        page = request.args.get('page', default=1, type=int)
        number = request.args.get('number', default=10, type=int)

        if page <= 0 or number <= 0:
            raise ParameterErrorException()
        from_ = page - 1
        res = es.search(
            index=User.es_index, doc_type=User.doc_type,
            body={'query': {'match_all': {}}},
            params={'from': from_, 'size': number}
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


api_v1_bp.add_url_rule('/user', view_func=UserAPI.as_view('user_api'))


class UserIdAPI(MethodView):
    def get(self, user_id):
        '''
        GET /api/v1/user/<user_id>
        '''
        res = es.get(index=User.es_index, doc_type=User.doc_type, id=user_id)
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
        User.delete(user_id)
        return jsonify(JsonResponse.success())


api_v1_bp.add_url_rule('/user/<int:user_id>', view_func=UserIdAPI.as_view('user_id_api'))
