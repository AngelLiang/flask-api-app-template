# coding=utf-8

import datetime as dt
from sqlalchemy import func, extract
from flask import abort

from apps.web.extensions import db
from apps.web.exceptions import APIException
from apps.web.utils import uncamelize


class ModelMixin(object):

    @classmethod
    def get_by_id(cls, record_id):
        if any((isinstance(record_id, str) and record_id.isdigit(),
                isinstance(record_id, (int, float))), ):
            model = cls.query.get(int(record_id))
            if model:
                return model
            else:
                # raise APIException(code=404)
                abort(404)
        else:
            raise APIException('参数错误！')

    @classmethod
    def create(cls, **kw):
        return cls(**kw)

    def update(self, attrs: list = None, exclude: list = None, commit=True, *args, **kw):
        """ update model

        :param attrs: 只更新这些字段
        :param exclude: 不需要更新的字段
        :param commit:
        """
        if attrs:
            for attr in attrs:
                value = kw.get(attr)
                if value is not None:
                    setattr(self, attr, value)
        else:
            for attr, value in kw.items():
                if exclude and attr in exclude:
                    # 排除不需要更新的字段
                    continue
                if value is not None:
                    setattr(self, attr, value)
        return commit and db.session.commit() or self


class TableStatisticsMixin(object):
    """数据库表统计方法混入类"""

    @classmethod
    def get_total(cls):
        return db.session.query(func.count('*')).select_from(cls).scalar()

    @classmethod
    def get_total_by_month(cls, month=None, year=None, attr='create_datetime'):
        """
        :param month: month
        :param year: year
        :param attr: The model attribute name for statistics.
                     The type is Datetime. Defualt is `create_datetime`

        :retType int: the total for model by month
        """
        if year is None:
            year = dt.date.today().year
        if month is None:
            month = dt.date.today().month
        sql_query = db.session.query(func.count('*')).filter(
            extract('year', getattr(cls, attr)) == year,
            extract('month', getattr(cls, attr)) == month
        )
        return sql_query.scalar()

    @classmethod
    def get_total_group_by_month(cls, year=None, attr='create_datetime'):
        """
        :param year: year
        :param attr: The model attribute name for statistics.
                     The type is Datetime. Defualt is `create_datetime`

        :retType tuple: (month, total)
        """
        if year is None:
            year = dt.date.today().year
        sql_query = db.session.query(
            extract('month', getattr(cls, attr)), func.count('*')
        ).filter(
            extract('year', getattr(cls, attr)) == year
        ).group_by(
            extract('month', getattr(cls, attr))
        )
        return sql_query.all()

    @classmethod
    def get_total_group_by_year(cls, attr='create_datetime'):
        """
        :param attr: The model attribute name for statistics.
                     The type is Datetime. Defualt is `create_datetime`

        :retType tuple: (year, total)
        """
        sql_query = db.session.query(
            extract('year', getattr(cls, attr)), func.count('*')
        ).group_by(
            extract('year', getattr(cls, attr))
        )
        return sql_query.all()
