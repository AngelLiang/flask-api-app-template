# codeing=utf-8

from flask import jsonify, current_app

from app.apis.v1 import api_v1_bp
from app.apis.v1.response_json import JsonResponse


class APIBaseException(ValueError):
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


@api_v1_bp.errorhandler(NotFoundException)
def not_found_handle(e):
    message = e.args[0] if e.args else None
    json_response = JsonResponse.not_found(message=message)
    return jsonify(json_response)


@api_v1_bp.errorhandler(ParameterMissException)
def parameter_miss_handle(e):
    message = e.args[0] if e.args else None
    json_response = JsonResponse.parameter_miss(message=message)
    return jsonify(json_response)


@api_v1_bp.errorhandler(ParameterErrorException)
def parameter_error_handle(e):
    message = e.args[0] if e.args else None
    json_response = JsonResponse.parameter_error(message=message)
    return jsonify(json_response)


@api_v1_bp.errorhandler(TokenTimeOutException)
def token_time_out_handle(e):
    message = e.args[0] if e.args else None
    json_response = JsonResponse.parameter_error(message=message)
    return jsonify(json_response)


@api_v1_bp.errorhandler(TokenErrorException)
def token_error_handle(e):
    message = e.args[0] if e.args else None
    json_response = JsonResponse.parameter_error(message=message)
    return jsonify(json_response)
