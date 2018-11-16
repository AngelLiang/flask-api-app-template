# codeing=utf-8

from flask import jsonify

from apps.web.utils import JsonResponse


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


__all__ = (
    APIBaseException,
    FailException,
    NotFoundException,
    ParameterMissException, ParameterErrorException,
    TokenTimeOutException, TokenErrorException
)


def register_errors(app):

    @app.errorhandler(APIBaseException)
    def api_base_error_handle(e):
        json_callback = JsonResponse.fail
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(FailException)
    def fail_handle(e):
        json_callback = JsonResponse.fail
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(NotFoundException)
    def not_found_handle(e):
        json_callback = JsonResponse.not_found
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(ParameterMissException)
    def parameter_miss_handle(e):
        json_callback = JsonResponse.parameter_miss
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(ParameterErrorException)
    def parameter_error_handle(e):
        json_callback = JsonResponse.parameter_error
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(TokenTimeOutException)
    def token_time_out_handle(e):
        json_callback = JsonResponse.token_timeout
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(TokenErrorException)
    def token_error_handle(e):
        json_callback = JsonResponse.token_error
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)
