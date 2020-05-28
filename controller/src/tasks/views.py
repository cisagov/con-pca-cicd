from datetime import datetime, timedelta

from celery.utils.log import get_logger
from celery.result import AsyncResult
from celery.task.control import revoke

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from config.celery import app
from .tasks import subscription_report
from .serializers import SubscriptionReportSerializer, TaskListSerializer


logger = get_logger(__name__)
inspect = app.control.inspect()


class TaskListView(APIView):
    @swagger_auto_schema(
        responses={"200": TaskListSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Subscription report generation tasks",
        operation_description="Return a list of scheduled subscription report generation tasks",
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
        serializer = TaskListSerializer(context)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={"200": SubscriptionReportSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Subscription report generation tasks",
        operation_description="Create a scheduled subscription report generation task",
    )
    def post(self, request):
        """
        Create a scheduled subscription report generation task. This is
        triggered by a GoPhish callback once a subscription has been created.
        """
        data = request.data
        subscription_uuid = data.get("subscription_uuid")
        # Execute task in 90 days from campaign launch
        ninety_days = datetime.utcnow() + timedelta(days=90)
        try:
            task = subscription_report.apply_async(
                args=[subscription_uuid], eta=ninety_days
            )
        except add.OperationalError as exc:
            logger.exception("Subscription task raised: %r", exc)
        context = {"task id": task.id, "subscription_uuid": subscription_uuid}
        return Response(context)


class TaskView(APIView):
    @swagger_auto_schema(
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

    @swagger_auto_schema(
        security=[],
        operation_id="Delete a task",
        operation_description="Delete a specific task by its task ID",
    )
    def delete(self, request, task_id):
        """
        Delete a specific task in the queue
        """
        revoke(task_id, terminate=True)
        return Response(f"Task {task_id} has been deleted")
