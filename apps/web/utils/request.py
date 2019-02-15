# coding=utf-8

from collections import UserDict

from flask import request
from werkzeug.datastructures import ImmutableMultiDictMixin

from apps.web.exceptions import APIException
from apps.web.utils.string import uncamelize, camelize


class RequestDict(UserDict, ImmutableMultiDictMixin):
    """请求参数dict"""

    def __init__(self, query_string=True, to_uncamelize=False, *args, **kw):
        super().__init__(*args, **kw)

        if query_string:
            self.update(request.args)
        if request.is_json:
            if to_uncamelize:
                # 驼峰转下划线
                reqest_json = {}
                reqest_json_ = request.json
                for key, value in reqest_json_.items():
                    reqest_json[uncamelize(key)] = value
            else:
                reqest_json = request.json
            self.update(reqest_json)
        elif request.values:
            self.update(request.values)

    def is_json(self):
        return request.is_json

    def get_json(self, *args):
        return request.get_json(*args)

    def must_json(self):
        if not request.is_json:
            raise APIException()

    def check(self, *args):
        """检查参数

        :para *arg: 参数列表
        """
        for arg in args:
            # 参数有该key且其value不能为空
            if not self.data.get(arg):
                raise APIException('参数错误！')

    def get_page(self, key='page', default=1):
        try:
            return self.data['_page']
        except KeyError:
            self.data['_page'] = request.values.get(key, default=1, type=int)
            return self.data['_page']

    def get_per_page(self, key='perPage', default=10):
        try:
            return self.data['_per_page']
        except KeyError:
            self.data['_per_page'] = request.values.get(key, default=default, type=int)
            return self.data['_per_page']

    def get_from_query_string(self, key, to_camelize=True):
        value = self.get(key)
        if value is None and to_camelize:
            value = self.get(camelize(key))
        return value
