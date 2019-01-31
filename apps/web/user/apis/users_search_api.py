# coding=utf-8
"""
用户查询接口
"""

from sqlalchemy import func

from flasgger.utils import swag_from

from flask import request, jsonify

from apps.web.extensions import db

from apps.web.exceptions import APIException

from apps.web.auth.decorator import api_login_required
from apps.web.user.models import User

from apps.web.user.apis import user_bp
from apps.web.user.apis.utils import user_to_dict, gen_links, gen_pagination
from apps.web.user.apis.utils import sort_list


@user_bp.route("/search/users", methods=["GET"])
@api_login_required
@swag_from('../docs/users_search_api/search_users.yml')
def search_users():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('perPage', default=10, type=int)
    q = request.values.get('q')         # 查询条件

    q_dict = {}
    try:
        if not q:
            raise APIException()
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
    sort = request.values.get('sort')   # 排序
    order = request.values.get('order')  # 顺序：`asc` or `desc`
    users_sql = sort_list(User, users_sql, sort, order)

    paginate = users_sql.paginate(page, per_page)

    # total = db.session.query(func.count('*')).filter_by(**q_dict).scalar()
    total = users_sql.count()

    data = []
    for user in paginate.items:
        item = user_to_dict(user)
        data.append(item)

    return jsonify({
        'pagination': gen_pagination(paginate.page, per_page, total),
        'links': gen_links(paginate, per_page),
        'data': data,
        'self': request.url
    })
