# coding=utf-8

from flask import jsonify, Blueprint

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
