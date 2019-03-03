# coding=utf-8
"""

- :exc:`Exception`
    - :exc:`~apps.web.exceptions.APIException`
"""


class APIException(Exception):
    def __init__(self, message='Client Error!', code=400, status_code=None):
        self.message = message
        self.code = code
        self.status_code = status_code if status_code is not None else code
