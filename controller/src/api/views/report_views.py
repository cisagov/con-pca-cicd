"""
Reports Views.

This handles the api for all the Reports urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.subscriptions_serializers import SubscriptionGetSerializer
from api.manager import CampaignManager
from api.utils.db_utils import get_single
from api.serializers.reports_serializers import ReportsGetSerializer


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
        operation_id="Get Subscription Report Details",
        operation_description=" This handles the API to get details on a Subscription Report",
    )
    def get(self, request, subscription_uuid):
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        campaigns = subscription.get("gophish_campaign_list")
        summary = [
            campaign_manager.get("summary", campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]
        target_count = sum([targets.get("stats").get("total") for targets in summary])
        context = {
            "subscription_uuid": subscription_uuid,
            "customer_name": subscription.get("name"),
            "start_date": summary[0].get("created_date"),
            "end_date": summary[0].get("send_by_date"),
            "target_count": target_count,
        }

        serializer = ReportsGetSerializer(context)
        return Response(serializer.data)
