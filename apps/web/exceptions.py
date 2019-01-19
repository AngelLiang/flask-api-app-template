# coding=utf-8
"""

- :exc:`ValueError`
    - :exc:`~apps.web.exceptions.APIException`
"""


class APIException(ValueError):
    def __init__(self, message='Client Error!', code=400):
        self.message = message
        self.code = code
