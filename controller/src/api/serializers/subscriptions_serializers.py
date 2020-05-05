"""
Subscription Serializers.

These are Django Rest Famerwork Serializers. These are used for
serializing data coming from the db into a request responce.
"""
# Third-Party Libraries
from rest_framework import serializers


class SubscriptionContactSerializer(serializers.Serializer):
    """
    This is the SubscriptionContact Serializer.

    This is a formats the data coming out of the Db.
    """

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    office_phone = serializers.CharField(max_length=100)
    mobile_phone = serializers.CharField(max_length=100)
    customer = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class SubscriptionTargetSerializer(serializers.Serializer):
    """
    This is the Target Serializer.

    This is a formats the data coming out of the Db.
    """

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    position = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class SubscriptionClicksSerializer(serializers.Serializer):
    """
    This is the SubscriptionClicks Serializer.

    This is a formats the data coming out of the Db.
    """

    source_ip = serializers.CharField(max_length=100)
    timestamp = serializers.DateTimeField()
    target_uuid = serializers.UUIDField()


class GoPhishCampaignsSerializer(serializers.Serializer):
    """
    This is the GoPhishCampaigns Serializer.

    This is a formats the data coming out of the Db.
    """

    campaign_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    email_template = serializers.CharField(max_length=100)
    landing_page_template = serializers.CharField(max_length=100)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    target_email_list = SubscriptionTargetSerializer(many=True)


class SubscriptionGetSerializer(serializers.Serializer):
    """
    This is the Subscription Serializer.

    This is a formats the data coming out of the Db.
    """

    # created by mongodb
    subscription_uuid = serializers.UUIDField()
    # values being passed in.
    customer_uuid = serializers.UUIDField()
    name = serializers.CharField(required=True, max_length=100)
    start_date = serializers.DateTimeField()
    gophish_campaign_list = GoPhishCampaignsSerializer(many=True)
    primary_contact = SubscriptionContactSerializer()
    additional_contact_list = SubscriptionContactSerializer(many=True)
    status = serializers.CharField(max_length=100)
    target_email_list = SubscriptionTargetSerializer(many=True)
    templates_selected_uuid_list = serializers.ListField(required=False)
    active = serializers.BooleanField()
    # db data tracking added below 
    created_by = serializers.CharField(max_length=100)
    cb_timestamp = serializers.DateTimeField()
    last_updated_by = serializers.CharField(max_length=100)
    lub_timestamp = serializers.DateTimeField()


class SubscriptionPostSerializer(serializers.Serializer):
    """
    This is the Subscription Post Request Serializer.

    This is a formats the data coming out of the Db.
    """

    customer_uuid = serializers.UUIDField()
    name = serializers.CharField(required=True, max_length=100)
    start_date = serializers.DateTimeField()
    gophish_campaign_list = GoPhishCampaignsSerializer(many=True)
    primary_contact = SubscriptionContactSerializer()
    additional_contact_list = SubscriptionContactSerializer(many=True)
    status = serializers.CharField(max_length=100)
    target_email_list = SubscriptionTargetSerializer(many=True)
    templates_selected_uuid_list = serializers.ListField()
    active = serializers.BooleanField()


class SubscriptionPostResponseSerializer(serializers.Serializer):
    """
    This is the Subscription Post Response Serializer.

    This is a formats the data coming out of the Db.
    """

    subscription_uuid = serializers.UUIDField()


class SubscriptionPatchSerializer(serializers.Serializer):
    """
    This is the Subscription PATCH Request Serializer.

    This is a formats the data coming out of the Db.
    """

    customer_uuid = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False, max_length=100)
    start_date = serializers.DateTimeField(required=False)
    gophish_campaign_list = GoPhishCampaignsSerializer(many=True, required=False)
    primary_contact = SubscriptionContactSerializer(required=False)
    additional_contact_list = SubscriptionContactSerializer(many=True, required=False)
    status = serializers.CharField(max_length=100, required=False)
    target_email_list = SubscriptionTargetSerializer(many=True, required=False)
    templates_selected_uuid_list = serializers.ListField(required=False)
    active = serializers.BooleanField(required=False)


class SubscriptionPatchResponseSerializer(serializers.Serializer):
    """
    This is the Subscription PATCH Response Serializer.

    This is a formats the data coming out of the Db.
    """

    customer_uuid = serializers.UUIDField()
    name = serializers.CharField(required=True, max_length=100)
    start_date = serializers.DateTimeField()
    gophish_campaign_list = GoPhishCampaignsSerializer(many=True)
    primary_contact = SubscriptionContactSerializer()
    additional_contact_list = SubscriptionContactSerializer(many=True)
    status = serializers.CharField(max_length=100)
    target_email_list = SubscriptionTargetSerializer(many=True)
    templates_selected_uuid_list = serializers.ListField(required=False)
    active = serializers.BooleanField()
    created_by = serializers.CharField(max_length=100)
    cb_timestamp = serializers.DateTimeField()
    last_updated_by = serializers.CharField(max_length=100)
    lub_timestamp = serializers.DateTimeField()


class SubscriptionDeleteResponseSerializer(serializers.Serializer):
    """
    This is the Subscription DELETE Response Serializer.

    This is a formats the data coming out of the Db.
    """

    subscription_uuid = serializers.UUIDField()
