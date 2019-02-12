# coding=utf-8

import datetime as dt
from sqlalchemy import inspect, desc
from flask import url_for, request
from apps.web.user.models import User


def user_to_dict(user: User):
    d = dict(
        id=user.id,
        username=user.username,
        isActive=user.is_active,
        state=user.state,
        createDatetime=dt.datetime.strftime(
            user.create_datetime, '%Y-%m-%d %H:%M:%S'),
        fullname=user.fullname,
        email=user.email,
        isEmailConfirm=user.is_email_confirm,
        phone=user.phone,
        isPhoneConfirm=user.is_phone_confirm,
        additionalInfo=user.additional_info,
    )
    links = dict()
    if not user.is_administrator():
        links['changeUserActive'] = url_for(
            'user_bp.user_is_active', user_id=user.id, _external=True)
    d['links'] = links
    return d


def gen_pagination(page, per_page, total=None):
    pagination = dict(
        page=page,
        perPage=per_page,
    )
    if total:
        pagination['total'] = total
    return pagination


def gen_links(paginate, per_page):
    """
    :param paginate:
    :param per_page:
    """
    links = {}
    if paginate.has_prev:
        links['prev_page_url'] = url_for(
            request.basu_url, page=paginate.prev_num, perPage=per_page, _external=True)
    if paginate.has_next:
        links['next_pape_url'] = url_for(
            request.basu_url, page=paginate.next_num, perPage=per_page, _external=True)
    return links


def sort_list(Model, sql, sort, order):
    """SQL排序
    :param Model: 模型
    :param sql: SQL语句
    :param sort: 要排序的column
    :param order: `asc` or 'desc'
    """
    insp = inspect(Model)
    columns = insp.columns
    if sort and sort in [c.name for c in columns]:
        if order == 'desc':
            sql = sql.order_by(desc(sort))
        else:
            sql = sql.order_by(sort)
    return sql
