"""
Reports Views.

This handles the api for all the Reports urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import (
    DeceptionLevelStatsModel,
    TemplateModel,
    validate_template,
)
from api.serializers.reports_serializers import (
    EmailReportsGetSerializer,
    ReportsGetSerializer,
)
from api.utils.db_utils import get_list, get_single
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from notifications.views import ReportsEmailSender
from reports.utils import (
    campaign_templates_to_string,
    get_cycles_breakdown,
    get_most_successful_campaigns,
    get_related_subscription_stats,
    get_reports_to_click,
    get_statistic_from_group,
    get_subscription_stats_for_cycle,
    get_template_details,
)
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
        """Get Method."""
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

        # boil it all down to a template name and a score in one object
        templates = {
            template.get("name"): template.get("deception_score")
            for template in template_list
        }

        # distribute statistics into deception levels
        levels = []
        levels.append(DeceptionLevelStatsModel("low", 1))
        levels.append(DeceptionLevelStatsModel("moderate", 2))
        levels.append(DeceptionLevelStatsModel("high", 3))

        for campaign in campaigns:
            level_number = campaign.get("deception_level")
            if level_number not in [1, 2, 3]:
                continue

            bucket = next(
                level for level in levels if level.level_number == level_number
            )
            bucket.sent = bucket.sent + campaign.get("phish_results", {}).get("sent", 0)
            bucket.clicked = bucket.clicked + campaign.get("phish_results", {}).get(
                "clicked", 0
            )
            bucket.opened = bucket.opened + campaign.get("phish_results", {}).get(
                "opened", 0
            )

        # aggregate statistics
        sent = sum(
            [campaign.get("phish_results", {}).get("sent", 0) for campaign in campaigns]
        )
        target_count = sum(
            [len(campaign.get("target_email_list")) for campaign in campaigns]
        )

        created_date = ""
        end_date = ""
        if campaigns:
            created_date = campaigns[0].get("created_date")
            end_date = campaigns[0].get("completed_date")

        start_date = subscription["start_date"]

        # Get statistics for the specified subscription during the specified cycle
        subscription_stats = get_subscription_stats_for_cycle(subscription, start_date)
        get_related_subscription_stats(subscription, start_date)
        get_cycles_breakdown(subscription["cycles"])

        # Get template details for each campaign template
        get_template_details(subscription_stats["campaign_results"])

        metrics = {
            "total_users_targeted": len(subscription["target_email_list"]),
            "number_of_email_sent_overall": get_statistic_from_group(
                subscription_stats, "stats_all", "sent", "count"
            ),
            "number_of_clicked_emails": get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "count"
            ),
            "number_of_opened_emails": get_statistic_from_group(
                subscription_stats, "stats_all", "opened", "count"
            ),
            "number_of_phished_users_overall": get_statistic_from_group(
                subscription_stats, "stats_all", "submitted", "count"
            ),
            "number_of_reports_to_helpdesk": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "count"
            ),
            "repots_to_clicks_ratio": get_reports_to_click(subscription_stats),
            "avg_time_to_first_click": get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "average"
            ),
            "avg_time_to_first_report": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "average"
            ),
            "most_successful_template": campaign_templates_to_string(
                get_most_successful_campaigns(subscription_stats, "reported")
            ),
        }

        context = {
            "customer_name": subscription.get("name"),
            "templates": templates,
            "start_date": created_date,
            "end_date": end_date,
            "levels": levels,
            "sent": sent,
            "target_count": target_count,
            "metrics": metrics,
        }
        serializer = ReportsGetSerializer(context)
        return Response(serializer.data)


class MonthlyReportsPDFView(APIView):
    """
    This is the MonthlyReportsView Pdf API Endpoint.

    This handles the API a Get request for download a pdf document
    """

    @swagger_auto_schema(
        responses={"200": ReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get Monthly Subscription Report PDF",
        operation_description="This downloads a subscription report PDF by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        api_host = request.get_host()
        html = HTML(f"http://{api_host}/reports/{subscription_uuid}/monthly/")
        html.write_pdf("/tmp/monthly_subscription_report.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("monthly_subscription_report.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="monthly_subscription_report.pdf"'
            return response


class CycleReportsPDFView(APIView):
    """
    This is the CycleReportsView Pdf API Endpoint.

    This handles the API a Get request for download a pdf document
    """

    @swagger_auto_schema(
        responses={"200": ReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get Subscription Cycle Report PDF",
        operation_description="This downloads a subscription report PDF by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        api_host = request.get_host()
        html = HTML(f"http://{api_host}/reports/{subscription_uuid}/cycle/")
        html.write_pdf("/tmp/subscription_cycle_report.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("subscription_cycle_report.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="subscription_cycle_report.pdf"'
            return response


class YearlyReportsPDFView(APIView):
    """
    This is the YearlyReportsView Pdf API Endpoint.

    This handles the API a Get request for download a pdf document
    """

    @swagger_auto_schema(
        responses={"200": ReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Get Yearly Subscription Report PDF",
        operation_description="This downloads a subscription report PDF by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        api_host = request.get_host()
        html = HTML(f"http://{api_host}/reports/{subscription_uuid}/yearly/")
        html.write_pdf("/tmp/yearly_subscription_report.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("yearly_subscription_report.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="yearly_subscription_report.pdf"'
            return response


class MonthlyReportsEmailView(APIView):
    """
    This is the ReportsView Email API Endpoint.

    This handles the API a Get request for emailing a reports document
    """

    @swagger_auto_schema(
        responses={"200": EmailReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Send Email Subscription Report PDF",
        operation_description="This sends a subscription report email by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        message_type = "monthly_report"

        # Send email
        sender = ReportsEmailSender(subscription, message_type)
        sender.send()

        serializer = EmailReportsGetSerializer({"subscription_uuid": subscription_uuid})
        return Response(serializer.data)


class CycleReportsEmailView(APIView):
    """
    This is the ReportsView Email API Endpoint.

    This handles the API a Get request for emailing a reports document
    """

    @swagger_auto_schema(
        responses={"200": EmailReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Send Email Subscription Report PDF",
        operation_description="This sends a subscription report email by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        message_type = "cycle_report"

        # Send email
        sender = ReportsEmailSender(subscription, message_type)
        sender.send()

        serializer = EmailReportsGetSerializer({"subscription_uuid": subscription_uuid})
        return Response(serializer.data)


class YearlyReportsEmailView(APIView):
    """
    This is the ReportsView Email API Endpoint.

    This handles the API a Get request for emailing a reports document
    """

    @swagger_auto_schema(
        responses={"200": EmailReportsGetSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Send Email Subscription Report PDF",
        operation_description="This sends a subscription report email by subscription uuid",
    )
    def get(self, request, subscription_uuid):
        """Get Method."""
        # subscription = get_single(
        #     subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        # )
        # message_type = "yearly_report"
        # Send email
        # sender = ReportsEmailSender(subscription, message_type)
        # sender.send()

        serializer = EmailReportsGetSerializer({"subscription_uuid": subscription_uuid})
        return Response(serializer.data)
