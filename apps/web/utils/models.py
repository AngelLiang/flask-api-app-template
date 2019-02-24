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
        """写入数据库"""
        if value is not None:
            if dialect.name == 'sqlite':
                value = json.dumps(value)   # 将dict转化成str格式
            elif dialect.name in ('postgresql', 'mysql'):
                pass
            else:
                if isinstance(value, dict):
                    value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """从数据库中读取"""
        if value is not None:
            if dialect.name == 'sqlite':
                value = json.loads(value)   # 将str转化成dict格式
            elif dialect.name in ('postgresql', 'mysql'):
                if isinstance(value, str):
                    value = json.loads(value)
            else:
                if isinstance(value, str):
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
