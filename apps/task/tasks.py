# coding=utf-8

import time
from . import celery


@celery.task
def async_task():
    print('Async!')
    time.sleep(5)
    print('Finish!')
