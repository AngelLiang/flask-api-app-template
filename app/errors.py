# codeing=utf-8

from flask import jsonify

from app.exceptions import APIException


def register_errors(app):

    @app.errorhandler(400)
    def error_400(e):
        return jsonify({
            'code': 400,
            'message': '客户端错误！'
        }), 400

    @app.errorhandler(401)
    def error_401(e):
        return jsonify({
            'code': 401,
            'message': '用户未认证！'
        }), 401

    @app.errorhandler(403)
    def error_403(e):
        return jsonify({
            'code': 403,
            'message': '禁止访问！'
        }), 403

    @app.errorhandler(404)
    def error_404(e):
        return jsonify({
            'code': 404,
            'message': '找不到资源！'
        }), 404

    @app.errorhandler(500)
    def error_500(e):
        return jsonify({
            'code': 500,
            'message': '服务器错误！'
        }), 500

    @app.errorhandler(APIException)
    def api_error_handle(e):
        return jsonify({
            'code': e.code,
            'message': e.message
        }), e.code

    # @app.errorhandler(Exception)
    # def exception_handle(e):
    #     return jsonify({
    #         'code': 500,
    #         'message': '服务器错误！'
    #     }), 500
