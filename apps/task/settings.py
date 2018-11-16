# coding=utf-8

import os

# Redis
# CELERY_BROKER_URL='redis://localhost:6379'
# CELERY_RESULT_BACKEND='redis://localhost:6379'

# RabbitMQ
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') or 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND') or 'amqp://guest:guest@localhost:5672//'

config_dict = dict(
    CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND
)
