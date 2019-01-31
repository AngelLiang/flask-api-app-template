# coding=utf-8

from flask import url_for
from apps.web.user.models import User


def user_to_dict(user: User):
    d = dict(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        state=user.state,
        create_datetime=user.create_datetime,
        fullname=user.fullname,
        email=user.email,
        is_email_confirm=user.is_email_confirm,
        phone=user.phone,
        is_phone_confirm=user.is_phone_confirm,
        additional_info=user.additional_info,
    )
    links = {
        'change_user_active': url_for('user_bp.user_is_active', user_id=user.id, _external=True)
    }
    d['links'] = links
    return d
