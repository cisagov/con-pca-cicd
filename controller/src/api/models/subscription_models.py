"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import (
    BooleanType,
    DateTimeType,
    EmailType,
    IntType,
    ListType,
    ModelType,
    StringType,
    UUIDType,
)


class SubscriptionContactModel(Model):
    """
    This is the SubscriptionContact Model.

    This is a format to hold contact information in the subscription model.
    """

    name = StringType()
    email = EmailType(required=True)


class SubscriptionTargetModel(Model):
    """
    This is the SubscriptionTarget Model.

    This is a format to hold target information in the subscription model.
    """

    target_uuid = UUIDType()
    status = StringType()
    sent_date = DateTimeType()


class SubscriptionClicksModel(Model):
    """
    This is the SubscriptionClicks Model.

    This is a format to hold target information in the subscription model.
    """

    source_ip = StringType()
    timestamp = DateTimeType()
    target_uuid = UUIDType()


class GoPhishCampaignsModel(Model):
    """
    This is the GoPhishCampaigns Model.

    This is a format to hold GophishCampaign information in the subscription model.
    """

    template_email_uuid = UUIDType()
    template_landing_page_uuid = UUIDType()
    start_date = DateTimeType()
    end_date = DateTimeType()
    target_email_list = ListType(ModelType(SubscriptionTargetModel))


class SubscriptionModel(Model):
    """
    This is the Subscription Model.

    This controls all data needed in saving the model.
    """

    subscription_uuid = UUIDType()
    customer_uuid = UUIDType()
    name = StringType()
    organization = StringType()
    start_date = DateTimeType()
    end_date = DateTimeType()
    report_count = IntType()
    gophish_campaign_list = ListType(ModelType(GoPhishCampaignsModel))
    first_report_timestamp = DateTimeType()
    primary_contact = ModelType(SubscriptionContactModel)
    additional_contact_list = ListType(ModelType(SubscriptionContactModel))
    status = StringType()
    target_email_list = ListType(UUIDType)
    click_list = ListType(ModelType(SubscriptionClicksModel))
    templates_selected = ListType(UUIDType)
    active = BooleanType()
    # db data tracking added below
    created_by = StringType()
    cb_timestamp = DateTimeType()
    last_updated_by = StringType()
    lub_timestamp = DateTimeType()


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
