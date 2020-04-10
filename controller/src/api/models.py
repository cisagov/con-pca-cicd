"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import BooleanType, DateTimeType, StringType, UUIDType
from schematics.types import DictType
from schematics.types.compound import ListType


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
    last_action = DateTimeType(required=False)
    start_date = DateTimeType(required=False)
    end_date = DateTimeType(required=False)
    active = BooleanType()


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
