"""Webhook View."""
# Standard Python Libraries
import asyncio
import logging

# Third-Party Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers import webhook_serializers
from api.utils import db_service
from drf_yasg.utils import swagger_auto_schema
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
        responses={"200": None, "400": "Bad Request",},
        security=[],
        operation_id="Incoming WebHook from gophish ",
        operation_description=" This handles incoming webhooks from GoPhish Campaigns.",
    )
    def post(self, request):
        """Post method."""
        data = request.data.copy()
        self.__handle_webhook_data(data)
        return Response()

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
            single_subscription = self.__get_campaign(seralized_data["campaign_id"])
            if seralized_data["message"] == "Campaign Created":
                print(
                    "campain created: {}".format(
                        single_subscription["subscription_uuid"]
                    )
                )
            elif seralized_data["message"] == "Email Sent":
                print("Sent email: {}".format(single_subscription["subscription_uuid"]))
            elif seralized_data["message"] == "Email Opened":
                print(
                    "Email Opened: {}".format(single_subscription["subscription_uuid"])
                )
            elif seralized_data["message"] == "Clicked Link":
                print(
                    "Clicked Link: {}".format(single_subscription["subscription_uuid"])
                )
            elif seralized_data["message"] == "Submitted Data":
                print(
                    "Submitted Data: {}".format(
                        single_subscription["subscription_uuid"]
                    )
                )
        else:
            print(data)
        return

    def __get_campaign(self, campaign_id):
        """Get Campaign Data."""
        parameters = {"gophish_campaign_list.campaign_id": campaign_id}
        print(parameters)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return next(iter(subscription_list), None)
