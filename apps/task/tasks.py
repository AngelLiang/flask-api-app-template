# coding=utf-8

import time
from celery.utils.log import get_task_logger

from flask_mail import Message

from apps.task import celery

from web import create_app
from web.extensions import mail

logger = get_task_logger(__name__)


@celery.task
def async_task():
    print('Async!')
    time.sleep(5)
    print('Finish!')


@celery.task
def send_email(subject, to, body='hello world!', **kw):
    """发送邮件任务
    :param subject: 主题
    :param to:      收件人
    :param body:    正文
    """
    logger.info('Ready to send Email...')
    web_app = create_app()
    with web_app.app_context():
        message = Message(subject, recipients=[to], body=body)
        mail.send(message)
    logger.info('Finish to send Email!')
