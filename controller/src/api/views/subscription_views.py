"""
This is the main views for api.

This handles api views
"""
# Standard Python Libraries
import asyncio
import logging
import uuid

# Third-Party Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.utils import db_service
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class SubscriptionsListView(APIView):
    """
    This is the SubscriptionsListView APIView.

    This handles the API to get a List of Subscriptions.
    """

    def get(self, request):
        """Get method."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription_list = loop.run_until_complete(service.filter_list(parameters={}))

        return Response(subscription_list)

    def post(self, request, format=None):
        """Post method."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        to_create = request.data.copy()
        to_create["subscription_uuid"] = str(uuid.uuid4())
        created_responce = loop.run_until_complete(service.create(to_create=to_create))
        logging.info("created responce {}".format(created_responce))
        if "errors" in created_responce:
            return Response(created_responce, status=status.HTTP_400_BAD_REQUEST)
        return Response(created_responce, status=status.HTTP_201_CREATED)


class SubscriptionView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Get a Substription with subscription_uuid.
    """

    def get(self, request, subscription_uuid):
        """Get method."""
        logging.debug("get subscription_uuid {}".format(subscription_uuid))
        print("get subscription_uuid {}".format(subscription_uuid))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)

        subscription = loop.run_until_complete(service.get(uuid=subscription_uuid))

        return Response(subscription)
