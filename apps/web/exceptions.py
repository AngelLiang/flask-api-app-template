# coding=utf-8
"""

- :exc:`Exception`
    - :exc:`~apps.web.exceptions.APIException`
        - :exc:`~apps.web.exceptions.FailException`
        - :exc:`~apps.web.exceptions.NotFoundException`
        - :exc:`~apps.web.exceptions.ParameterMissingException`
        - :exc:`~apps.web.exceptions.ParameterErrorException`
        - :exc:`~apps.web.exceptions.TokenTimeOutException`
        - :exc:`~apps.web.exceptions.TokenErrorException`
"""


class APIException(Exception):
    def __init__(self, message=None):
        self.message = message


class FailException(APIException):
    pass


class NotFoundException(APIException):
    pass


class ParameterMissingException(APIException):
    pass


class ParameterErrorException(APIException):
    pass


class TokenTimeOutException(APIException):
    pass


class TokenErrorException(APIException):
    pass
