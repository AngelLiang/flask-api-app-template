# coding=utf-8

from flask import Blueprint
from flask_cors import CORS

api_v1_bp = Blueprint("api_v1", __name__)

CORS(api_v1_bp)

from app.apis.v1 import auth
