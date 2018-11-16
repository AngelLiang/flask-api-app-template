# coding=utf-8

from functools import wraps

from flask import jsonify, request

from apps.web.utils import JsonResponse
from apps.web.auth.apis import get_token, validate_token


def api_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 因为在CORS交互中的事先请求（Pre-flight Request）会使用OPTIONS方法发送请求，
        # 所以我们只在OPTIONS方法之外的请求中验证令牌。
        if request.method != 'OPTIONS':
            token = get_token()
            ret = validate_token(token)
            if not ret:
                return jsonify(JsonResponse.fail(u"用户未登录！"))
            return func(*args, **kwargs)
    return decorated_function
