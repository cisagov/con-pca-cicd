"""
Reports Views.

This handles the api for all the Reports urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
# Local Libraries
# Django Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
from api.serializers.reports_serializers import ReportsGetSerializer
from api.utils.db_utils import get_list, get_single
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()


class ReportsView(APIView):
    """
    This is the ReportsView API Endpoint.

    This handles the API a Get .
    """

    @swagger_auto_schema(
        responses={"200": ReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get Subscription Report data",
        operation_description="This fetches a subscription's report data by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        subscription_uuid = self.kwargs["subscription_uuid"]
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        campaigns = subscription.get("gophish_campaign_list")
        parameters = {
            "template_uuid": {"$in": subscription["templates_selected_uuid_list"]}
        }
        template_list = get_list(
            parameters, "template", TemplateModel, validate_template,
        )

        templates = {
            template.get("name"): template.get("deception_score")
            for template in template_list
        }
        summary = [
            campaign_manager.get("summary", campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]

        sent = sum([targets.get("stats").get("sent", 0) for targets in summary])
        opened = sum([targets.get("stats").get("opened", 0) for targets in summary])
        clicked = sum([targets.get("stats").get("clicked", 0) for targets in summary])
        target_count = sum([targets.get("stats").get("total") for targets in summary])

        created_date = ""
        end_date = ""
        if len(summary):
            created_date = summary[0].get("created_date")
            end_date = summary[0].get("end_date")

        context = {
            "customer_name": subscription.get("name"),
            "templates": templates,
            "start_date": created_date,
            "end_date": end_date,
            "sent": sent,
            "opened": opened,
            "clicked": clicked,
            "target_count": target_count,
        }
        serializer = ReportsGetSerializer(context)
        return Response(serializer.data)


class ReportsPDFView(APIView):
    """
    This is the ReportsView Pdf API Endpoint.

    This handles the API a Get request for download a pdf document
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
