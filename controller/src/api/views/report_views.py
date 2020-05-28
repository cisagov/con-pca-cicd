"""
Reports Views.

This handles the api for all the Reports urls.
"""
# Standard Python Libraries
import logging

# Django Libraries
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, FileResponse

# Third-Party Libraries
from weasyprint import HTML
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Libraries
from api.serializers.reports_serializers import ReportsGetSerializer


logger = logging.getLogger(__name__)


class ReportsView(APIView):
    """
    This is the ReportsView API Endpoint.

    This handles the API a Get .
    """

    @swagger_auto_schema(
        responses={"200": ReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get Subscription Report PDF",
        operation_description="This downloads a subscription report PDF by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        html = HTML(f"http://localhost:8000/reports/{subscription_uuid}/")
        html.write_pdf("/tmp/subscription_report.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("subscription_report.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="subscription_report.pdf"'
            return response
