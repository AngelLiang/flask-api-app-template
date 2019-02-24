# coding=utf-8

from collections import UserDict

from flask import request
from werkzeug.datastructures import ImmutableMultiDictMixin

from apps.web.exceptions import APIException
from apps.web.utils.string import uncamelize, uncamelize_for_dict_key


class RequestDict(UserDict, ImmutableMultiDictMixin):
    """请求参数dict"""

    def __init__(self, query_string=True, to_uncamelize=False, *args, **kw):
        super().__init__(*args, **kw)

        if query_string:
            self._query_string = {}
            self._query_string.update(request.args)
            if to_uncamelize:
                # 驼峰转下划线
                self._query_string.update(uncamelize_for_dict_key(request.args))
            self.update(self._query_string)
        if request.is_json:
            self._json = {}
            if to_uncamelize:
                # 驼峰转下划线
                self._json.update(uncamelize_for_dict_key(request.json))
            else:
                self._json.update(request.json)
            self.update(self._json)
        elif request.values:
            request_values = request.values
            self.update(request_values)

    def is_json(self):
        return request.is_json

    def get_json(self, to_uncamelize=True, *args, **kw):
        """
        :param to_uncamelize: 驼峰转下换线
        """
        requset_json = request.get_json(*args, **kw)
        if to_uncamelize:
            return uncamelize_for_dict_key(requset_json)
        else:
            return requset_json

    def must_json(self):
        if not request.is_json:
            raise APIException()

    def check(self, *args):
        """检查参数

        :param *arg: 参数列表

        :retType list: 各个传入参数key的value
        """
        value_list = []
        for arg in args:
            # 参数有该key且其value不能为None或空字符串
            v = self.data.get(arg)
            if v is None or v == '':
                raise APIException('参数错误！')
            value_list.append(v)
        return value_list

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

    def get_from_query_string(self, key, to_uncamelize=True, *arg, **kw):
        if to_uncamelize:
            value = self.get(uncamelize(key), *arg, **kw)
        else:
            value = self.get(key, *arg, **kw)
        return value

    def get_order(self):
        return self.get('order')

    def get_sort(self):
        return self.get('sort')

    def get_include(self)->list:
        """获取响应需要包含的字段

        最多200个字符长度
        """
        include = self.get('include')
        if include:
            return include[:200].split(',')

    def get_exclude(self)->list:
        """获取响应需要排除的字段

        最多200个字符长度
        """
        exclude = self.get('exclude')
        if exclude:
            return exclude[:200].split(',')
