# coding=utf-8
# flake8: noqa
"""
Run:

    celery worker -A apps.task.celery -l info -c 1

Shell Test:

    celery shell -A apps.task.celery
    >>> task.apply_async(('data', )).get(timeout=3)
    >>> send_email.apply_async(('hello', 'email@mail.com')).get(timeout=3)

"""

import os
import sys

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, BASEDIR)

# 加载环境变量
from flask.cli import load_dotenv
load_dotenv()

from celery import Celery
# settings
from apps.task.settings import config_dict


celery = Celery(__name__)
celery.conf.update(config_dict)

from . import tasks
