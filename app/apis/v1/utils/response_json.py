# coding=utf-8
"""
json response生成类
"""

from flask import request


def _update_url(d: dict):
    d.update({"request": request.base_url})


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
    def success(message="Success!", code=20000, data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def fail(message="Fail", code=40000, data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def not_found(message="Not Found!", code=40004, data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def parameter_miss(message="Parameter Miss", code=40001,  data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def parameter_error(message="Parameter Error!", code=40012,  data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def token_timeout(message="Token Timeout!", code=40021, data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d

    @staticmethod
    def token_error(message="Token Error!", code=40022, data={}) -> dict:
        d = dict(code=code, message=message, data=data)
        _update_url(d)
        return d
