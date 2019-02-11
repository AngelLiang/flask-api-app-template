# coding=utf-8

from flask import request
from werkzeug.datastructures import ImmutableMultiDictMixin

from apps.web.exceptions import APIException


class RequestDict(dict, ImmutableMultiDictMixin):
    """请求参数dict"""

    def __init__(self):
        if request.is_json:
            self.request_dict = request.get_json()
        elif request.values:
            self.request_dict = request.values
        else:
            self.request_dict = None
            raise APIException('请求参数格式错误！')

    def __repr__(self):
        return repr(self.request_dict)

    def __getitem__(self, value):
        """
        Usage:

            ```
            request_dict = RequestDict()
            value = request_dict['key']
            ```
        """
        return self.request_dict[value]

    def is_json(self):
        return request.is_json

    def check(self, *args):
        """检查参数

        :para *arg: 参数列表
        """
        for arg in args:
            # 参数有该key且其value不能为空
            if not self.request_dict.get(arg):
                raise APIException()

    def to_dict(self):
        return self.request_dict
