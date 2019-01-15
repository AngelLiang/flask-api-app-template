# coding=utf-8


class WebException(object):

    class APIBaseException(Exception):
        def __init__(self, message=None):
            self.message = message

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
