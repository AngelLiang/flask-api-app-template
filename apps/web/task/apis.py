# coding=utf-8

from flask import jsonify, Blueprint
from flask import request

from apps.web.utils import JsonResponse

task_bp = Blueprint('task_bp', __name__)


@task_bp.route("/task/async", methods=["GET", "POST"])
def task_async():
    from apps.task.tasks import async_task
    async_task.delay()
    return jsonify(JsonResponse.success())


@task_bp.route("/task/async2", methods=["GET", "POST"])
def task_async2():
    from apps.task.tasks import async_task
    async_task.apply_async()
    return jsonify(JsonResponse.success())


@task_bp.route("/task/send-email", methods=["GET", "POST"])
def send_email():
    email = request.values.get('email')
    from apps.task.tasks import send_email
    if email:
        send_email.apply_async(('hello', email))
        return jsonify(JsonResponse.success(message='send email to ' + email))
    return jsonify(JsonResponse.fail())
