"""
Sending Profile Serializers.

These are Django Rest Framework Serializers. These are used for
serializing data coming from the db into a request response.
"""
# Third-Party Libraries
from rest_framework import serializers


class SendingProfileSerializer(serializers.Serializer):
    """
    This is the Sending Profile Serializer.
    """

    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    host = serializers.CharField()
    interface_type = serializers.CharField()
    from_address = serializers.CharField()
    ignore_cert_errors = serializers.BooleanField()
    modified_date = serializers.CharField()
    # headers = serializers.CharField()


class SendingProfilePatchSerializer(serializers.Serializer):
    """
    This is the Sending Profile Serializer.
    """

    name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    host = serializers.CharField(max_length=255, required=False)
    interface_type = serializers.CharField(required=False)
    from_address = serializers.CharField(required=False)
    ignore_cert_errors = serializers.BooleanField(required=False)
    modified_date = serializers.CharField(required=False)
    # headers = serializers.CharField(required=False)


class SendingProfilePatchResponseSerializer(serializers.Serializer):
    """
    This is the Sending Profile Serializer.
    """

    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    host = serializers.CharField(max_length=255)
    interface_type = serializers.CharField()
    from_address = serializers.CharField()
    ignore_cert_errors = serializers.BooleanField()
    modified_date = serializers.CharField()
    # headers = serializers.CharField()


class SendingProfileDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class SendingProfileDeleteResponseSerializer(serializers.Serializer):
    """
    """

    id = serializers.IntegerField()
