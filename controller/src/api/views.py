"""
This is the main views for api.

This handles api views
"""
# Standard Python Libraries
import asyncio
import logging
import uuid

# Third-Party Libraries
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SubscriptionModel, validate_subscription
from .utils import db_service

logger = logging.getLogger(__name__)


class SubscriptionsView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Substriptions.
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
