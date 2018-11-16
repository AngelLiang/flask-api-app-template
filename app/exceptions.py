# coding=utf-8
class APIBaseException(ValueError):
    pass


class FailException(APIBaseException):
    pass


class NotFoundException(APIBaseException):
    pass


class ParameterMissException(APIBaseException):
    pass


class ParameterErrorException(APIBaseException):
    pass


class TokenTimeOutException(APIBaseException):
    pass


class TokenErrorException(APIBaseException):
    pass
