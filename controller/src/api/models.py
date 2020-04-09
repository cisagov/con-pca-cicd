"""Models."""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import DateTimeType, StringType, UUIDType


class SubscriptionModel(Model):
    """
    This is an example Model.

    This shows basic types that we will use on each model.
    """

    subscription_uuid = UUIDType()
    name = StringType()
    enum_type = StringType(required=True, choices=("initial", "post", "pre", "final"))
    record_tstamp = DateTimeType(required=True)
    method_of_record_creation = StringType()
    last_updated_by = StringType(required=False, max_length=255)
    lub_timestamp = DateTimeType(required=False)
    method_of_lu = StringType(required=False)


def validate_subscription(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return SubscriptionModel(data_object).validate()
