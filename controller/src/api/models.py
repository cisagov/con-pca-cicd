"""Models."""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import BooleanType, DateTimeType, StringType, UUIDType


class SubscriptionModel(Model):
    """
    This is the Subscription Model.

    This controls all data needed in saving the model.
    """

    subscription_uuid = UUIDType()
    name = StringType()
    status = StringType()
    primary_contact = StringType()
    customer = StringType()
    last_action = DateTimeType(required=False)
    active = BooleanType()


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
