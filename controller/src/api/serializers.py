from datetime import datetime

from rest_framework import serializers


class SubscriptionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=200)
    primary_contact = serializers.CharField(max_length=200)
    customer = serializers.CharField(max_length=200)
    last_action = serializers.DateField()
    active = serializers.BooleanField

        return subscription
