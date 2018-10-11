# codeing=utf-8

from flask import jsonify, current_app, g

from app.apis.v1 import api_v1_bp
from app.apis.v1.utils import JsonResponse


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


@api_v1_bp.errorhandler(APIBaseException)
def api_base_error_handle(e):
    json_callback = JsonResponse.fail
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(FailException)
def fail_handle(e):
    json_callback = JsonResponse.fail
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(NotFoundException)
def not_found_handle(e):
    json_callback = JsonResponse.not_found
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(ParameterMissException)
def parameter_miss_handle(e):
    json_callback = JsonResponse.parameter_miss
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(ParameterErrorException)
def parameter_error_handle(e):
    json_callback = JsonResponse.parameter_error
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(TokenTimeOutException)
def token_time_out_handle(e):
    json_callback = JsonResponse.token_timeout
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)


@api_v1_bp.errorhandler(TokenErrorException)
def token_error_handle(e):
    json_callback = JsonResponse.token_error
    if e.args:
        json_response = json_callback(message=e.args[0])
    else:
        json_response = json_callback()
    return jsonify(json_response)
