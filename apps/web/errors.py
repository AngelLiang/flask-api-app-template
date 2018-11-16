# codeing=utf-8

from flask import jsonify

from apps.web.utils import JsonResponse
from apps.web import exceptions  # noqa


def register_errors(app):

    @app.errorhandler(exceptions.APIBaseException)
    def api_base_error_handle(e):
        json_callback = JsonResponse.fail
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.FailException)
    def fail_handle(e):
        json_callback = JsonResponse.fail
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.NotFoundException)
    def not_found_handle(e):
        json_callback = JsonResponse.not_found
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.ParameterMissException)
    def parameter_miss_handle(e):
        json_callback = JsonResponse.parameter_miss
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.ParameterErrorException)
    def parameter_error_handle(e):
        json_callback = JsonResponse.parameter_error
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.TokenTimeOutException)
    def token_time_out_handle(e):
        json_callback = JsonResponse.token_timeout
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)

    @app.errorhandler(exceptions.TokenErrorException)
    def token_error_handle(e):
        json_callback = JsonResponse.token_error
        if e.args:
            json_response = json_callback(message=e.args[0])
        else:
            json_response = json_callback()
        return jsonify(json_response)
