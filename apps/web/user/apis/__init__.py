# coding=utf-8

from apps.web.extensions import CORS
from flask import Blueprint

user_bp = Blueprint("user_bp", __name__)
CORS(user_bp)

from . import common_api
from . import rest_api
from . import search_api
