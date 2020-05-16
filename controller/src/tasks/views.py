from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from config.celery import app
from .tasks import campaign_report
from .serializers import CampaignReportSerializer


inspect = app.control.inspect()


class TaskListView(APIView):
    @swagger_auto_schema(
        responses={"200": CampaignReportSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Campaign report generation tasks",
        operation_description="Return a list of scheduled campaign report generation task",
    )
    def get(self, request):
        """
        View a list of active, scheduled, reserved
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

    @swagger_auto_schema(
        responses={"200": CampaignReportSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Campaign report generation tasks",
        operation_description="Create a scheduled campaign report generation task",
    )
    def post(self, request):
        """
        Create a scheduled campaign report generation task. This is
        triggered by a GoPhish callback once a campaign has been created.
        """
        data = request.data
        word = data.get("word")
        task = campaign_report.apply_async(args=[word], countdown=30)
        context = {"task id": task.id, "word": word}
        return Response(context)


class TaskView(APIView):
    @swagger_auto_schema(
        responses={"200": CampaignReportSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get a specific task's details",
        operation_description="Query a specific task by its ID to return specific details",
    )
    def get(self, request, task_id):
        """
        Get details on a specific task by its ID
        """
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }

        return Response(result)
