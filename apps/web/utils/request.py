# coding=utf-8

import copy
from collections import UserDict

from flask import Request, request
from werkzeug.datastructures import ImmutableMultiDictMixin

from apps.web.exceptions import APIException
from apps.web.utils.string import uncamelize, uncamelize_for_dict_key
from apps.web.utils.override import override


class CustomRequest(Request):

    @override
    def args(self):
        data = super().args
        return data

    def get_args(self, to_uncamelize=False):
        data = super().args
        if to_uncamelize:
            data = uncamelize_for_dict_key(data)
        return data

    def get_values(self, to_uncamelize=False):
        data = super().values
        if to_uncamelize:
            data = uncamelize_for_dict_key(data)
        return data

    @override
    def get_json(self, to_uncamelize=False, *args, **kw):
        data = super().get_json(self, *args, **kw)
        if to_uncamelize:
            data = uncamelize_for_dict_key(data)
        return data


class RequestDict(UserDict, ImmutableMultiDictMixin):
    """请求参数dict"""

    def __init__(self, query_string=True, to_uncamelize=False, *args, **kw):
        super().__init__(*args, **kw)

        if query_string:
            self._args = request.args
            # request.args 是 ImmutableMultiDict() 类型，因此,
            # 如果使用update方法，新dict value 是一个字符串数组
            # self._args.update(request.args)
            if to_uncamelize:
                self._args.update(uncamelize_for_dict_key(self._args))
            self.update(self._args)
        if request.is_json:
            self._json = request.json
            if to_uncamelize:
                self._json.update(uncamelize_for_dict_key(self._json))
            self.update(self._json)
        elif request.values:
            self._values = request.values
            if to_uncamelize:
                self._values.update(uncamelize_for_dict_key(self._values))
            self.update(self._values)

    def is_json(self):
        return request.is_json

    def get_json(self, to_uncamelize=True, *args, **kw):
        """
        :param to_uncamelize: 驼峰转下换线
        """
        data = request.get_json(*args, **kw)
        if to_uncamelize:
            return uncamelize_for_dict_key(data)
        else:
            return data

    def must_json(self):
        if not request.is_json:
            raise APIException()

    def check(self, *args):
        """检查参数

        :param *arg: 参数列表

        :retType list: 各个传入参数key的value
        """
        lst = []
        try:
            for arg in args:
                # 参数有该key且其value不能为None
                v = self.data[arg]
                if v is None:
                    raise APIException(f'{arg}参数不能为空！')
                lst.append(v)
        except KeyError:
            raise APIException(f'缺少{arg}参数！')
        return lst

    def get_page(self, key='page', default=1):
        # requset.values 本身有缓存
        return request.values.get(key, default=1, type=int)

    def get_per_page(self, key='perPage', default=10):
        # requset.values 本身有缓存
        return request.values.get(key, default=default, type=int)

    def get_order(self):
        return self.get('order')

    def get_sort(self):
        return self.get('sort')

    def get_include(self) -> list:
        """获取响应需要包含的字段

        最多200个字符长度
        """
        include = self.get('include')
        if include:
            return include[:200].split(',')

    def get_exclude(self) -> list:
        """获取响应需要排除的字段

        最多200个字符长度
        """
        exclude = self.get('exclude')
        if exclude:
            return exclude[:200].split(',')
