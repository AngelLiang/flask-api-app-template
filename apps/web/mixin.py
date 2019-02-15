# coding=utf-8

from apps.web.exceptions import APIException
from apps.web.utils import uncamelize


class ModelMixin(object):
    @classmethod
    def get_by_id(cls, id_):
        try:
            model = cls.query.get(int(id_))
        except ValueError:
            raise APIException('参数错误！')
        else:
            if model:
                return model
            raise APIException(code=404)

    @classmethod
    def create(cls, **kw):
        return cls(**kw)

    def update(self, **kw):
        for attr, value in kw.items():
            setattr(self, uncamelize(attr), value)
        return self
