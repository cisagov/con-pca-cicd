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
    first_name = StringType(required=True)
    last_name = StringType(required=True)
    office_phone = StringType(required=True)
    mobile_phone = StringType()
    customer = StringType()
    email = EmailType(required=True)
    """

    first_name = StringType(required=True)
    last_name = StringType(required=True)
    office_phone = StringType(required=True)
    mobile_phone = StringType()
    customer = StringType()
    email = EmailType(required=True)


class SubscriptionTargetModel(Model):
    """
    This is the Target Model.

    This controls all data needed in saving the model. Current fields are:
    first_name = StringType()
    last_name = StringType()
    position = StringType()
    email = EmailType(required=True)
    """

    first_name = StringType()
    last_name = StringType()
    position = StringType()
    email = EmailType(required=True)


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

    campaign_id = IntType()
    name = StringType()
    email_template = StringType()
    landing_page_template = StringType()
    start_date = DateTimeType()
    end_date = DateTimeType()
    target_email_list = ListType(ModelType(SubscriptionTargetModel))


class SubscriptionModel(Model):
    """
    This is the Subscription Model.

    This controls all data needed in saving the model.
    """

    # created by mongodb
    subscription_uuid = UUIDType()
    # values being passed in.
    customer_uuid = UUIDType()
    name = StringType()
    url = StringType()
    keywords = StringType()
    start_date = DateTimeType()
    # commented out fields for now are unused for the time
    # end_date = DateTimeType()
    # report_count = IntType()
    gophish_campaign_list = ListType(ModelType(GoPhishCampaignsModel))
    # first_report_timestamp = DateTimeType()
    primary_contact = ModelType(SubscriptionContactModel)
    additional_contact_list = ListType(ModelType(SubscriptionContactModel))
    status = StringType()
    target_email_list = ListType(ModelType(SubscriptionTargetModel))
    # click_list = ListType(ModelType(SubscriptionClicksModel))
    templates_selected_uuid_list = ListType(StringType)
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
