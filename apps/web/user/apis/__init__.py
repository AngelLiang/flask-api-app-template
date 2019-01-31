# coding=utf-8
# flake8: noqa
from apps.web.extensions import CORS
from flask import Blueprint

user_bp = Blueprint("user_bp", __name__)
CORS(user_bp)

from . import apis
from . import user_api
from . import users_api
from . import users_search_api
