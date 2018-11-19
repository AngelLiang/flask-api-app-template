from app.extensions import es


class ModelMixin(object):
    """
    必须实现`es_index`和`doc_type`属性。
    """

    @classmethod
    def get(cls, id):
        res = es.get(index=cls.es_index, doc_type=cls.doc_type, id=id)
        return res

    @classmethod
    def create(cls, **kw):
        res = es.create(index=cls.es_index, doc_type=cls.doc_type, id=id, body=kw)
        return res

    @classmethod
    def update(cls, id, *args, **kw):
        res = es.index(index=cls.es_index, doc_type=cls.doc_type, id=id, body=kw)
        return res

    @classmethod
    def delete(cls, id):
        res = es.delete(index=cls.es_index, doc_type=cls.doc_type, id=id)
        return res
