# coding=utf-8
"""
用户查询接口
"""
from sqlalchemy import func
from flasgger.utils import swag_from
from flask import request, jsonify

from apps.web.exceptions import APIException
from apps.web.utils import RequestDict, ResponseJson
from apps.web.utils import gen_links, gen_pagination, sort_list
from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User, user_to_dict
from apps.web.user.apis import user_bp


@user_bp.route("/search/users", methods=["GET"])
@api_login_required
@swag_from('../docs/users_search_api/search_users.yml')
def search_users():
    request_dict = RequestDict()
    page = request_dict.page
    per_page = request_dict.per_page

    request_dict.check('q')
    q = request_dict['q']        # 查询条件

    q_dict = {}
    try:
        q_list = q.split('+')
        for item in q_list:
            key, value = item.split(':')
            q_dict[key] = value
    except ValueError:
        raise APIException()

    # users_sql = db.session.query(User).filter_by(**q_dict)
    users_sql = User.query.filter_by(**q_dict)
    # users_sql = User.query.filter(text(q_filter))

    # 排序
    sort = request_dict.get('sort')   # 排序
    order = request_dict.get('order')  # 顺序：`asc` or `desc`
    users_sql = sort_list(User, users_sql, sort, order)

    paginate = users_sql.paginate(page, per_page)

    # total = db.session.query(func.count('*')).filter_by(**q_dict).scalar()
    total = users_sql.count()

    items = []
    for user in paginate.items:
        item = user_to_dict(user)
        items.append(item)

    return ResponseJson(
        data=items,
        links=gen_links(paginate, per_page),
        pagination=gen_pagination(paginate.page, per_page, total)
    )
