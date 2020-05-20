"""
Reports Serializers.

These are Django Rest Framework Serializers. These are used for
serializing data coming from the db into a request response.
"""
# Third-Party Libraries
from rest_framework import serializers


class ReportsGetSerializer(serializers.Serializer):
    """
    This is the Reports Serializer.

    This formats the data returned
    from the reports api call
    """

    subscription_uuid = serializers.UUIDField()
    customer_name = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    target_count = serializers.IntegerField()
