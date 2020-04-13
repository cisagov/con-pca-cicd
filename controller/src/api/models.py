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

    uuid = UUIDType()
    status = StringType()
    sent_date = DateTimeType()


class SubscriptionModel(Model):
    """
    This is the Subscription Model.

    This controls all data needed in saving the model. Current fields are:
    subscription_uuid
    organziation,
    primary contact,
    additional contacts,
    status,
    target emails list,
    templates selected,
    start date,
    end date,
    active
    """

    subscription_uuid = UUIDType()
    organziation = StringType()
    primary_contact = ModelType(SubscriptionContactModel)
    additional_contact_list = ListType(ModelType(SubscriptionContactModel))
    status = StringType()
    target_email_list = ListType(ModelType(SubscriptionTargetModel))
    templates_selected = ListType(UUIDType)
    start_date = DateTimeType()
    end_date = DateTimeType()
    active = BooleanType()


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
