# coding=utf-8


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
