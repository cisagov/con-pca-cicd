from celery.result import AsyncResult, current_app
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery import app
from .tasks import campaign_report

inspect = app.control.inspect()


class TaskListView(APIView):
    def get(self, request):
        """
        Return a list of active, scheduled, reserved
        and registered tasks. Also specifies which celery worker
        the task will be executed on
        """
        context = {
            "active": inspect.active(),
            "scheduled": inspect.scheduled(),
            "reserved": inspect.reserved(),
            "registered": inspect.registered(),
        }
        return Response(context)

    def post(self, request):
        data = request.data
        word = data.get("word")
        task = campaign_report.apply_async(args=[word], countdown=30)
        context = {"task id": task.id, "word": word}
        return Response(context)


class TaskView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }

        return Response(result)
