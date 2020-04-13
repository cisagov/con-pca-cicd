"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import DictType, IntType, StringType, UUIDType


class TemplateModel(Model):
    """
    This is the Template Model.

    This controls all data needed in saving the model. Current fields are:
    template_uuid
    system_path,
    name,
    deception_score,
    descriptive_words
    """

    template_uuid = UUIDType()
    name = StringType()
    system_path = StringType()
    deception_score = IntType()
    descriptive_words = DictType(IntType)


def validate_template(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return TemplateModel(data_object).validate()
