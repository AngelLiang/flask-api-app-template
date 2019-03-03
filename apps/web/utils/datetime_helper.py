# coding=utf-8

import datetime as dt
# import pytz
from functools import partial


def datetime_format(datetime: dt.datetime):
    # 末尾加Z表示UTC时间
    return datetime.isoformat() + 'Z'


# utc_tz = pytz.timezone('UTC')
# generate_datetime_now_with_tz = partial(dt.datetime.now, tz=utc_tz)
