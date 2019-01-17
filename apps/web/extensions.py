# coding=utf-8

from flask import request


from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, LazyString


db = SQLAlchemy()
cors = CORS()

template = dict(
    host=LazyString(lambda: request.host),
    base_url=LazyString(lambda: request.base_url)
)
swagger = Swagger(template=template)
