# coding=utf-8

from sqlalchemy import func
from flasgger.utils import swag_from
from flask import request, jsonify, g

from apps.web.extensions import db
from apps.web.exceptions import APIException
from apps.web.utils import RequestDict, ResponseJson
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User
from apps.web.user.apis import user_bp


@user_bp.route("/users/info", methods=["GET"])
@api_login_required
@swag_from('../docs/common_api/user_info.yml')
def user_info():
    requset_dict = RequestDict()
    include = requset_dict.get_include() or ('roles',)  # 默认添加roles字段
    exclude = requset_dict.get_exclude()
    current_user = g.current_user
    data = current_user.to_dict(include=include, exclude=exclude)
    return ResponseJson(data=data)


@user_bp.route("/user/change-password", methods=['POST'])
@api_login_required
@swag_from('../docs/common_api/user_change_password.yml')
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

    return '', 204


@user_bp.route("/user/<int:user_id>/isActive", methods=['POST', 'PUT'])
@user_bp.route("/users/<int:user_id>/active", methods=['POST', 'PUT'])
@api_login_required
@swag_from('../docs/common_api/user_is_active.yml')
def user_is_active(user_id):
    """帐号的启用与禁用，管理员可用

        user_id: int, 用户id
        isActive:
        active:   bool, True - 启用
                        False - 禁用
    """
    user = User.get_by_id(user_id)
    request_dict = RequestDict()
    is_active = request_dict.get('isActive')
    if is_active is None:
        is_active = request_dict.get('active')
    if is_active is None:
        raise APIException('参数错误！')

    # if user.is_administrator() and is_active is False:
    #     raise APIException('管理员不能被禁用！', code=400)

    user.is_active = is_active
    db.session.add(user)
    db.session.commit()
    data = {'isActive': is_active}
    return jsonify(dict(data=data))
