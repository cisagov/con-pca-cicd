"""Webhook View."""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers import campaign_serializers, webhook_serializers
from api.serializers.subscriptions_serializers import (
    SubscriptionPatchResponseSerializer,
)
from api.utils.db_utils import get_single_subscription_webhook, update_single_webhook
from api.utils.template_utils import format_ztime
from drf_yasg.utils import swagger_auto_schema
from notifications.views import SubscriptionNotificationEmailSender
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)
manager = CampaignManager()


class IncomingWebhookView(APIView):
    """
    This is the a Incoming Webhook View.

    This handles Incoming Webhooks from gophish.
    """

    @swagger_auto_schema(
        request_body=webhook_serializers.InboundWebhookSerializer,
        responses={"202": SubscriptionPatchResponseSerializer, "400": "Bad Request",},
        security=[],
        operation_id="Incoming WebHook from gophish ",
        operation_description=" This handles incoming webhooks from GoPhish Campaigns.",
    )
    def post(self, request):
        """Post method."""
        data = request.data.copy()
        logger.debug(
            f"webhook post: campaign - {data['campaign_id']} | message - {data['message']}"
        )
        print("WEB HOOK HIT------------------------------------------")
        print(data)
        return self.__handle_webhook_data(data)

    def __update_phishing_results(self, webhook_data, phishing_result):
        """
        Update phishing result data based of provided webhook data.

        Accepts the webhook data to update off of, and the phishing reults to update
        """
        if webhook_data["message"] == "Email Sent":
            phishing_result["sent"] += 1
        if webhook_data["message"] == "Email Opened":
            phishing_result["opened"] += 1
        if webhook_data["message"] == "Clicked Link":
            phishing_result["clicked"] += 1
        if webhook_data["message"] == "Submitted Data":
            phishing_result["submitted"] += 1
        if webhook_data["message"] == "Email Reported":
            phishing_result["reported"] += 1
        return phishing_result

    def __update_cycle(self, webhook_data, subscription):
        for cycle in subscription["cycles"]:
            if cycle["active"]:
                self.__update_phishing_results(webhook_data, cycle["phish_results"])

    def is_duplicate_timeline_entry(self, timeline, webhook_data):
        """
        Check if webhook data is already registered in the timeline data.
        """
        for moment in timeline:
            if (
                moment["message"] == webhook_data["message"]
                and moment["email"] == webhook_data["email"]
            ):
                return True
        return False

    def __handle_webhook_data(self, data):
        """
        Handle Webhook Data.

        The Webhook doesnt give us much besides:
        campaign_id = serializers.IntegerField()
        email = serializers.EmailField()
        time = serializers.DateTimeField()
        message = serializers.CharField()
        details = serializers.CharField()

        But using this, we can call the gophish api and update out db on each
        webhook event.
        """
        if "message" in data:
            seralized = webhook_serializers.InboundWebhookSerializer(data)
            seralized_data = seralized.data
            subscription = get_single_subscription_webhook(
                seralized_data["campaign_id"],
                "subscription",
                SubscriptionModel,
                validate_subscription,
            )
            if subscription is None:
                return Response(status=status.HTTP_404_NOT_FOUND)

            campaign_event = seralized_data["message"]
            if campaign_event in [
                "Email Sent",
                "Email Opened",
                "Clicked Link",
                "Submitted Data",
                "Email Reported",
            ]:
                gophish_campaign = manager.get(
                    "campaign", campaign_id=seralized_data["campaign_id"]
                )
                gophish_campaign_serialized = campaign_serializers.CampaignSerializer(
                    gophish_campaign
                )
                is_duplicate = True
                gophish_campaign_data = gophish_campaign_serialized.data
                if (
                    subscription["status"] == "Queued"
                    and campaign_event == "Email Sent"
                ):
                    sender = SubscriptionNotificationEmailSender(
                        subscription, "subscription_started"
                    )
                    sender.send()
                    subscription["status"] = "In Progress"
                    logger.info(
                        "Subscription Notification email sent: {}".format(
                            subscription["subscription_uuid"]
                        )
                    )

                for campaign in subscription["gophish_campaign_list"]:
                    if campaign["campaign_id"] == seralized_data["campaign_id"]:
                        is_duplicate = self.is_duplicate_timeline_entry(
                            campaign["timeline"], seralized_data
                        )
                        campaign["timeline"].append(
                            {
                                "email": seralized_data["email"],
                                "message": seralized_data["message"],
                                "time": format_ztime(seralized_data["time"]),
                                "details": seralized_data["details"],
                                "duplicate": is_duplicate,
                            }
                        )
                        if not is_duplicate:
                            self.__update_phishing_results(
                                data, campaign["phish_results"]
                            )
                            self.__update_cycle(data, subscription)
                        campaign["results"] = gophish_campaign_data["results"]
                        campaign["status"] = gophish_campaign_data["status"]

            updated_response = update_single_webhook(
                subscription=subscription,
                collection="subscription",
                model=SubscriptionModel,
                validation_model=validate_subscription,
            )
            if "errors" in updated_response:
                return Response(updated_response, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscriptionPatchResponseSerializer(updated_response)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_200_OK)
