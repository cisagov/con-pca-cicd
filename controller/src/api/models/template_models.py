"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Third-Party Libraries
from database.repository.models import Model
from database.repository.types import (
    BooleanType,
    DateTimeType,
    DictType,
    IntType,
    ListType,
    StringType,
    UUIDType,
)


class TemplateModel(Model):
    """
    This is the Template Model.

    This controls all data needed in saving the model. Current fields are:
    template_uuid
    system_path,
    name,
    deception_score,
    descriptive_words
    description [string]
    display_link [string]
    from_address [string]
    retired [bool]
    subject [string]
    text [string]
    topic [list] [string]
    grammer [int]
    link_domain [int]
    logo_graphics [int]
    external [int]
    internal [int]
    authoritative [int]
    organization [int]
    public_news [int]
    fear [int]
    duty_obligation [int]
    curiosity [int]
    greed [int]
    """

    template_uuid = UUIDType()
    name = StringType()
    system_path = StringType()
    deception_score = IntType()
    descriptive_words = DictType(IntType)
    description = StringType()
    display_link = StringType()
    from_address = StringType()
    retired = BooleanType()
    subject = StringType()
    text = StringType()
    topic_list = ListType(StringType)
    grammer = IntType()
    link_domain = IntType()
    logo_graphics = IntType()
    external = IntType()
    internal = IntType()
    authoritative = IntType()
    organization = IntType()
    public_news = IntType()
    fear = IntType()
    duty_obligation = IntType()
    curiosity = IntType()
    greed = IntType()
    # db_tracting data added below
    created_by = StringType()
    cb_timestamp = DateTimeType()
    last_updated_by = StringType()
    lub_timestamp = DateTimeType()


def validate_template(data_object):
    """
    This is an the validate_subscription.

    This shows basic validation for the model.
    """
    return TemplateModel(data_object).validate()
