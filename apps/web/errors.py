# codeing=utf-8

from flask import jsonify

from apps.web.utils import JsonResponse
from apps.web.exceptions import APIException, FailException
from apps.web.exceptions import NotFoundException
from apps.web.exceptions import ParameterErrorException, ParameterMissingException
from apps.web.exceptions import TokenErrorException, TokenTimeOutException


def _get_json_response(e, json_callback):
    message = getattr(e, 'message')
    if message:
        json_response = json_callback(message=message)
    else:
        json_response = json_callback()
    return json_response


def register_errors(app):

    @app.errorhandler(APIException)
    def api_base_error_handle(e):
        json_callback = JsonResponse.fail
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(FailException)
    def fail_handle(e):
        json_callback = JsonResponse.fail
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(NotFoundException)
    def not_found_handle(e):
        json_callback = JsonResponse.not_found
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(ParameterMissingException)
    def parameter_miss_handle(e):
        json_callback = JsonResponse.parameter_miss
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(ParameterErrorException)
    def parameter_error_handle(e):
        json_callback = JsonResponse.parameter_error
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(TokenTimeOutException)
    def token_time_out_handle(e):
        json_callback = JsonResponse.token_timeout
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)

    @app.errorhandler(TokenErrorException)
    def token_error_handle(e):
        json_callback = JsonResponse.token_error
        json_response = _get_json_response(e, json_callback)
        return jsonify(json_response)
