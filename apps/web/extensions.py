# coding=utf-8
# flake8: noqa

from flask_mail import Mail
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
cors = CORS()
db = SQLAlchemy()
