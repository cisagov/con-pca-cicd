"""
This is the main views for api.

This handles api views
"""
# Standard Python Libraries
import asyncio

# Third-Party Libraries
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import SubscriptionModel, validate_subscription
from .utils import db_service


class SubscriptionsView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Substriptions.
    """

    def get(self, request):
        """Get method."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscriptions", SubscriptionModel, validate_subscription)
        subscription_list = loop.run_until_complete(service.filter_list(parameters={}))

        return Response(subscription_list)

    def post(self, request, format=None):
        """Post method."""
        serializer = serializers.SubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
