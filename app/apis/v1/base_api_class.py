# coding=utf-8
"""
RESTful API base class
"""

import json
from flask import Blueprint, jsonify, request, current_app
from flask.views import MethodView

# db
from app.extensions import db
from sqlalchemy import func

# errors
from app.apis.v1.errors import ParameterMissException, ParameterErrorException, NotFoundException
# auth
from app.apis.v1.auth import api_login_required
# utils
from app.apis.v1.utils import JsonResponse
from app.apis.v1.utils import paginate_to_dict


BASE_URL = ""
BASE_ENDPOINT_NAME = ""


class ModelAPIMixin(object):
    # decorators = [api_login_required]

    Model = None

    def update_model(self, model):
        raise RuntimeError("You must implement this.")

    def query_model(self):
        """
        :return: paginate or None

        usage:

        ```
        def query_model(self):
            q = request.values.get("q")
            if q:
                q_json = json.loads(q)
                name = q_json.get("name")
                if name:
                    paginate = self.Model.query.filter(
                        self.Model.name.like(name+"%")).paginate(page, number)
                    return paginate
        ```

        """
        pass


class BaseModelAPI(MethodView):
    decorators = [api_login_required]


class ModelCountAPI(BaseModelAPI):

    def get(self):
        count = db.session.query(func.count('*')).select_from(
            self.Model).scalar()
        data = {"count": count}
        return jsonify(JsonResponse.success(data=data))


class ModelListAPI(BaseModelAPI):
    """
    Model需要实现`to_dict()`方法。

    usage:

    ```
    class TheModelAPIMixin(ModelAPIMixin):
        Model = the_model

        def update_model(self, model):
            pass

        def query_model(self):
            pass

    class TheModelListAPI(ModelListAPI, TheModelAPIMixin):
        pass
    ```

    """

    def get(self):
        # get parameter
        page = request.values.get("page", type=int, default=1)
        number = request.values.get("number", type=int, default=20)

        paginate = self.query_model()
        if paginate is None:
            paginate = self.Model.query.paginate(page, number)
        items = paginate.items
        data = paginate_to_dict(paginate)

        #  query count
        total_items = db.session.query(func.count('*')).select_from(
            self.Model).scalar()
        data["total_items"] = total_items
        # generate response
        return jsonify(JsonResponse.success(data=data))

    def post(self):
        model = self.Model()
        model = self.update_model(model)
        db.session.add(model)
        db.session.commit()
        data = model.to_dict()
        return jsonify(JsonResponse.success(data=data))


class ModelAPI(BaseModelAPI):

    def get(self, id: int):
        model = self.Model.query.get(id)
        if model is None:
            raise NotFoundException()
        data = model.to_dict()
        return jsonify(JsonResponse.success(data=data))

    def put(self, id: int):
        model = self.Model.query.get(id)
        if model is None:
            model = self.Model(id=id)
        model = self.update_model(model)
        db.session.add(model)
        db.session.commit()
        data = model.to_dict()
        return jsonify(JsonResponse.success(data=data))

    def delete(self, id: int):
        model = self.Model.query.get(id)
        if model is None:
            raise NotFoundException()
        db.session.delete(model)
        db.session.commit()
        return jsonify(JsonResponse.success())
