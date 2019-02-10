# coding=utf-8

from flask import request

from apps.web.exceptions import APIException


def get_request_parameter():
    if not request.is_json:
        raise APIException()
    return request.get_json()
