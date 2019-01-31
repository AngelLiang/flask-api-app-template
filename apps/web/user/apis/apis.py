# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from

from flask import request, jsonify
from flask import g

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User


from apps.web.user.apis import user_bp


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

    return jsonify(), 204


@user_bp.route("/user/<user_id>/is_active", methods=['POST'])
@api_login_required
@swag_from('../docs/user_is_active.yml')
def user_is_active(user_id):
    """帐号的启用与禁用，管理员可用

    requset path：
        user_id: 用户id
    request body:
        is_active: bool, True - 启用
                         False - 禁用
    """

    try:
        user = User.query.get(int(user_id))
    except ValueError:
        raise APIException()

    request_json = request.get_json()
    if not request_json:
        raise APIException()
    try:
        is_active = request_json['is_active']
    except KeyError:
        raise APIException()
    user.is_active = is_active
    db.session.add(user)
    db.session.commit()
    return jsonify({'is_active': is_active})
