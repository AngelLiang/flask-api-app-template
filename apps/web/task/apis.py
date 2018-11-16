# coding=utf-8

from flask import jsonify, Blueprint
# utils
from apps.web.utils import JsonResponse

task_bp = Blueprint('task_bp', __name__)


@task_bp.route("/task/async", methods=["GET", "POST"])
def task_async():
    from apps.task.tasks import async_task
    async_task.delay()
    return jsonify(JsonResponse.success())
