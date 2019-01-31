# coding=utf-8


def paginate2dict(paginate, items=None, total=None):
    d = {
        "items": items or [item.to_dict() for item in paginate.items],
        "items_size": len(paginate.items),
        "current_page": paginate.page,  # 当前页数
        "total_pages": paginate.pages,  # 总页数
        "has_prev": paginate.has_prev,  # 是否有前一页
        "has_next": paginate.has_next,  # 是否有下一页
        "prev_page": paginate.prev_num,   # 前一页数
        "next_page": paginate.next_num,   # 后一页数
    }
    if total:
        d['items_total'] = total
    return d
