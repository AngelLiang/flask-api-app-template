# coding=utf-8

from sqlalchemy import inspect, desc
from flask import url_for, request


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
