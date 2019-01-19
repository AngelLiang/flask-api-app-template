# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import request, jsonify

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User


from . import user_bp


@user_bp.route("/user/total", methods=["GET"])
@api_login_required
@swag_from('../docs/user_total.yml')
def user_total():
    total = db.session.query(func.count('*')).select_from(User).scalar()
    data = {'total': total}
    return jsonify(data)


@user_bp.route("/user/change-password", methods=['POST'])
@api_login_required
@swag_from('../docs/user_change_password.yml')
def user_change_password():
    """用户修改密码接口"""
    request_json = request.get_json()
    if not request_json:
        raise APIException()

    try:
        old_password = request_json['old_password']
        new_password = request_json['new_password']
        new_password_confirm = request_json['new_password_confirm']
    except KeyError:
        raise APIException()

    if new_password != new_password_confirm:
        raise APIException('两次密码不一致！')

    user = g.current_user
    if user.validate_password(old_password):
        user.set_password(new_password)

    return jsonify()


@user_bp.route("/user/active", methods=['POST'])
@api_login_required
@swag_from('../docs/user_is_active.yml')
def user_is_active():
    """帐号的启用与禁用，管理员可用
    格式：json
    参数：
        user_id: 用户id
        active: bool, True - 启用
                      False - 禁用
    """
    request_json = request.get_json()
    if not request_json:
        raise APIException()

    try:
        user_id = request_json['user_id']
        active = request_json['active']
    except KeyError:
        raise APIException()
    else:
        user = get_user_by_id(user_id)
        user.is_active = active
        db.session.add(user)
        db.session.commit()
        return jsonify()
