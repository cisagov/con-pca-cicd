"""Cycle View."""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.cycle_serializers import CycleEmailReportedListSerializer
from api.utils.db_utils import get_single
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CycleReportedView(APIView):
    """
    This is the Cycle Email reported View.

    This handles the list of emails reported in each cycle.
    """

    @swagger_auto_schema(
        responses={"200": CycleEmailReportedListSerializer, "400": "Bad Request"},
        operation_id="Get Reported Emails",
        operation_description="This handles the API for the Get a list of all email reported in a Subscription cycle with subscription_uuid.",
        tags=["CycleEmailReports"],
    )
    def get(self, request, subscription_uuid):
        """Get Method.

        Args:
            request (object): request object
            subscription_uuid (string): subscription_uuid

        Returns:
            object: Django Responce object
        """
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        # first get list of id's that are in the active cycle, then filter out the emails

        list_data = subscription["gophish_campaign_list"]
        reports_per_campaign = []
        for campaign in list_data:
            timeline = campaign["timeline"]
            filtered_list = [d for d in timeline if d["message"] == "Email Reported"]
            reported_emails = []
            for item in filtered_list:
                reported_emails.append(
                    {
                        "campaign_id": campaign["campaign_id"],
                        "email": item["email"],
                        "datetime": item["time"],
                    }
                )
            reports_per_campaign.append(
                {
                    "campaign_id": campaign["campaign_id"],
                    "reported_emails": reported_emails,
                }
            )

        cycles = subscription["cycles"]
        master_list = []
        for c in cycles:
            emails_reported_per_cycle = []
            c_list = c["campaigns_in_cycle"]
            for reports in reports_per_campaign:
                if reports["campaign_id"] in c_list:
                    emails_reported_per_cycle.extend(reports["reported_emails"])

            cycle_reported_emails = {
                "start_date": c["start_date"],
                "end_date": c["end_date"],
                "email_list": emails_reported_per_cycle,
            }
            master_list.append(cycle_reported_emails)

        serializer = CycleEmailReportedListSerializer(master_list, many=True)
        return Response(serializer.data)
