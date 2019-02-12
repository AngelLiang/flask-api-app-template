# coding=utf-8

import json
from json.decoder import JSONDecodeError
from sqlalchemy import JSON

from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.ext.mutable import MutableDict


# from apps.web.extensions import db


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict()

    """

    impl = Text

    def load_dialect_impl(self, dialect):
        """自定义Column实现
        - sqlite使用Text类型
        - postgresql和mysql 5.7.8+使用json类型
        """
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(Text())
        elif dialect.name in ('postgresql', 'mysql'):
            return dialect.type_descriptor(JSON())
        else:
            return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# Usage:
#
#   ```
#   class Model(Base):
#       ...
#       additional_json = Column(JsonType)
#   ```
JsonType = MutableDict.as_mutable(JSONEncodedDict)
