# codeing=utf-8

from flask import jsonify, request, render_template

from apps.web.exceptions import APIException


def is_accept_json():
    return request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html \
        or request.path.startswith('/api')


def register_errors(app):

    @app.errorhandler(400)
    def error_400(e):
        return jsonify(code=400, message='Client Error!'), 400

    @app.errorhandler(401)
    def error_401(e):
        return jsonify(code=401, message='Unauthorized!'), 401

    @app.errorhandler(403)
    def error_403(e):
        return jsonify(code=403, message='Forbidden!'), 403

    @app.errorhandler(404)
    def error_404(e):
        if is_accept_json():
            return jsonify(code=404, message='Not Found!'), 404
        return render_template('errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(422)
    def error_422(e):
        return jsonify(code=422, message='Unprocessable Entity!'), 422

    @app.errorhandler(500)
    def error_500(e):
        return jsonify(code=500, message='Server Error!'), 500

    @app.errorhandler(APIException)
    def api_error_handle(e):
        return jsonify(code=e.code, message=e.message), e.status_code


# def invalid_token():
#     response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid.')
#     response.headers['WWW-Authenticate'] = 'Bearer'
#     return response


# def token_missing():
#     response = api_abort(401)
#     response.headers['WWW-Authenticate'] = 'Bearer'
#     return response
