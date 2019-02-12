# coding=utf-8

from flask import request
from werkzeug.datastructures import ImmutableMultiDictMixin

from apps.web.exceptions import APIException


class RequestDict(dict, ImmutableMultiDictMixin):
    """请求参数dict"""

    def __init__(self):
        self.request_dict = {}
        self.get_paginate()
        self.request_dict['page'] = self.page
        self.request_dict['per_page'] = self.per_page

        if request.is_json:
            self.request_dict.update(request.json)
        elif request.values:
            self.request_dict.update(request.values)

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

    def get_paginate(self):
        self.page = request.args.get('page', default=1, type=int)
        self.per_page = request.args.get('perPage', default=10, type=int)

    def is_json(self):
        return request.is_json

    def check(self, *args):
        """检查参数

        :para *arg: 参数列表
        """
        for arg in args:
            # 参数有该key且其value不能为空
            if not self.request_dict.get(arg):
                raise APIException('参数错误！')

    def to_dict(self):
        return self.request_dict
