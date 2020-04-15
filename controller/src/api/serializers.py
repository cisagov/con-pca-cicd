from datetime import datetime

from rest_framework import serializers

from .utils import Subscription

class SubscriptionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=200)
    primary_contact = serializers.CharField(max_length=200)
    customer = serializers.CharField(max_length=200)
    last_action = serializers.DateField()
    active = serializers.BooleanField

    def create(self, validated_data):
        subscription = Subscription(
            name=validated_data.get('name'),
            status=validated_data.get('status'),
            primary_contact=validated_data.get('primary_contact'),
            customer=validated_data.get('customer'),
            last_action=validated_data.get('last_action'),
            active=validated_data.get('active')
        )
        return subscription
