# coding=utf-8
"""

- :exc:`Exception`
    - :exc:`~apps.web.exceptions.APIException`
"""


class APIException(Exception):
    def __init__(self, message='Client Error!', code=400):
        self.message = message
        self.code = code
