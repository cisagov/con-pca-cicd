"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Standard Python Libraries
import datetime

# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import (
    BooleanType,
    DateTimeType,
    DictType,
    ListType,
    StringType,
    UUIDType,
)


class SubscriptionModel(Model):
    """
    This is the Subscription Model.

    This controls all data needed in saving the model.
    """

    subscription_uuid = UUIDType()
    organziation = StringType()
    name = StringType()
    status = StringType()
    primary_contact = StringType()
    additional_contacts = ListType(DictType(StringType))
    customer = StringType()
    last_action = DateTimeType(default=datetime.datetime.now)
    start_date = DateTimeType(required=False)
    end_date = DateTimeType(required=False)
    active = BooleanType()


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
