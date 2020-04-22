"""
Customer Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import DateTimeType, StringType, UUIDType


class CustomerModel(Model):
    """
    This is the Customer Model.

    This controls all data needed in saving the model. Current fields are:
    customer_uuid
    name,

    """

    customer_uuid = UUIDType()
    name = StringType()

    # db_tracting data added below
    created_by = StringType()
    cb_timestamp = DateTimeType()
    last_updated_by = StringType()
    lub_timestamp = DateTimeType()


def validate_customer(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return CustomerModel(data_object).validate()
