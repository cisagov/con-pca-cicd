"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import DateTimeType, EmailType, StringType, UUIDType


class TargetModel(Model):
    """
    This is the Target Model.

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

    target_uuid = UUIDType()
    customer_uuid = UUIDType()
    first_name = StringType()
    last_name = StringType()
    email = EmailType(required=True)
    # db tracking added below.
    created_by = StringType()
    cb_timestamp = DateTimeType()
    last_updated_by = StringType()
    lub_timestamp = DateTimeType()


def validate_target(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return TargetModel(data_object).validate()
