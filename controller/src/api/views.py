import json
from datetime import datetime, date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .utils import Subscription


class SubscriptionsView(APIView):
    def get(self, request):

        subscriptions = Subscription(
            name="SC-1031.Matt-Daemon.1.1",
            status="Waiting on SRF",
            primary_contact="Matt Daemon",
            customer="Some Company.2com",
            last_action=date.today(),
            active=True
        )

        serializer = serializers.SubscriptionSerializer(subscriptions)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)