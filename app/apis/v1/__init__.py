# coding=utf-8
# flake8: noqa

from flask import Blueprint
from app.extensions import CORS

api_v1_bp = Blueprint("api_v1", __name__)

CORS(api_v1_bp)

from . import auth
from . import user
