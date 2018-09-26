# coding=utf-8
"""
json response生成类
"""

from flask import request


def _update_url(d: dict):
    d["request"] = request.base_url


response_dict = {
    "success": {
        "code": 20000,
        "message": "Success!"
    },
    "fail": {
        "code": 40000,
        "message": "Fail!"
    },
    "not_found": {
        "code": 40004,
        "message": "Not Found!"
    },
    "parameter_miss": {
        "code": 40011,
        "message": "Parameter Miss!"
    },
    "parameter_error": {
        "code": 40012,
        "message": "Parameter Error!"
    },
    "token_time_out": {
        "code": 40000,
        "message": "Token Time Out!"
    },
    "token_error": {
        "code": 40000,
        "message": "Token Error!"
    }
}


class JsonResponse(object):
    """
    usage:

    ```
    JsonResponse.success()
    ```

    """

    ##########################################################################
    # make method

    @staticmethod
    def success(message=None, data=None) -> dict:
        key_name = "success"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def fail(message=None, data=None) -> dict:
        key_name = "fail"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def not_found(message=None, data=None)->dict:
        key_name = "not_found"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def parameter_miss(message=None, data=None) -> dict:
        key_name = "parameter_miss"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def parameter_error(message=None, data=None) -> dict:
        key_name = "parameter_error"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def token_time_out(message=None, data=None) -> dict:
        key_name = "token_time_out"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d

    @staticmethod
    def token_error(message=None, data=None) -> dict:
        key_name = "token_error"
        code = response_dict[key_name]["code"]
        msg = message or response_dict[key_name]["message"]
        data = data or {}
        d = dict(code=code, message=msg, data=data)
        _update_url(d)
        return d
