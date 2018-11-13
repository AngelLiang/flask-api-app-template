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
            body={
                'query': {'match_all': {}},
                "sort": {"create_datetime": "asc"}  # 默认使用 create_datetime 正序排序。desc：倒序
            },
            params={'from': from_, 'size': number}  # 分页
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
    def get(self, id_):
        '''
        GET /api/v1/user/<id_>
        '''
        res = es.get(index=User.es_index, doc_type=User.doc_type, id=id_)
        current_app.logger.debug(res)
        data = res
        return jsonify(JsonResponse.success(data=data))

    def post(self, id_):
        '''
        POST /api/v1/user/<id_>
        '''
        username = request.values.get('username')
        password = request.values.get('password')

        data = User.update(id_, username, password)
        return jsonify(JsonResponse.success(data=data))

    def delete(self, id_):
        '''
        DELETE /api/v1/user/<id_>
        '''
        User.delete(id_)
        return jsonify(JsonResponse.success())


api_v1_bp.add_url_rule('/user/<id_>', view_func=UserIdAPI.as_view('user_id_api'))
