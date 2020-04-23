"""Webhook View."""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.manager import CampaignManager
from api.serializers import webhook_serializers
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
        event = data["message"]
        print(event)
        return
