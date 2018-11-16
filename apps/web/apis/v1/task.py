# coding=utf-8

from flask import jsonify
# blueprint
from apps.web.apis.v1 import api_v1_bp
# utils
from apps.web.apis.v1.utils import JsonResponse


@api_v1_bp.route("/task/async", methods=["GET", "POST"])
def task_async():
    from apps.task.tasks import async_task
    async_task.delay()
    return jsonify(JsonResponse.success())
