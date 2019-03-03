# coding=utf-8

from functools import wraps
from flask import request, g
from apps.web.auth.utils import get_token, validate_token


def api_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 因为在CORS交互中的事先请求（Pre-flight Request）会使用OPTIONS方法发送请求，
        # 所以我们只在OPTIONS方法之外的请求中验证令牌。
        if request.method != 'OPTIONS':
            token, token_type = get_token()
            user = validate_token(token)
            g.current_user = user  # 将用户对象存储到g上
            return func(*args, **kwargs)
    return decorated_function
