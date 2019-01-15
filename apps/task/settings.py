# coding=utf-8

import os
from kombu import Exchange

BASEDIR = os.path.realpath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

# ### 默认队列配置 ###
task_default_queue = 'flask-api-app-tempalte'
task_default_exchange = 'flask-api-app-tempalte'
# task_default_routing_key = 'flask-api-app-tempalte'

# delivery_mode: =1，message不写入磁盘；=2（默认）message会写入磁盘
default_exchange = Exchange('flask-api-app-tempalte', delivery_mode=1)

# ### 配置时区
timezone = 'Asia/Shanghai'

# ### RabbitMQ
broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

# ### 防止内存泄漏
# 默认每个worker跑完10个任务后，自我销毁程序重建来释放内存
worker_max_tasks_per_child = 10

config_dict = dict(
    # flask调用任务似乎也需要指定该队列，否则没有发送到celery该默认队列
    # task_default_queue=task_default_queue,
    task_default_exchange=task_default_exchange,
    # task_default_routing_key=task_default_routing_key
    # tasks_queues=tasks_queues,
    # task_routes=task_routes,

    timezone=timezone,
    # beat_schedule=beat_schedule,
    # beat_max_loop_interval=beat_max_loop_interval,
    # beat_dburi=beat_dburi,

    broker=broker_url,
    result_backend=result_backend,
    # result_persistent=result_persistent,

    worker_max_tasks_per_child=worker_max_tasks_per_child
)
