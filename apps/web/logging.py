# coding=utf-8

import queue
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import QueueHandler, QueueListener


def register_logger(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        'logs/flask-app.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_queue_logger(app):

    que = queue.Queue(-1)  # no limit on size
    queue_handler = QueueHandler(que)
    handler = logging.StreamHandler()
    listener = QueueListener(que, handler)
    root = logging.getLogger()

    root.addHandler(queue_handler)
    formatter = logging.Formatter('%(threadName)s: %(message)s')
    handler.setFormatter(formatter)

    listener.start()
    # The log output will display the thread which generated
    # the event (the main thread) rather than the internal
    # thread which monitors the internal queue. This is what
    # you want to happen.
    root.warning('Look out!')

    # listener.stop()
