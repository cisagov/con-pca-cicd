"""
Models.

These are not Django Models, there are created using Schematics Models
"""
# Local Libraries
from database.repository.models import Model
from database.repository.types import (
    DateTimeType,
    IntType,
    ModelType,
    StringType,
    UUIDType,
)
from api.models.template_models import (
    TemplateAppearanceModel,
    TemplateSenderModel,
    TemplateRelevancyModel,
    TemplateBehaviorModel,
)


class RecommendationModel(Model):
    """
    This is the Recommendation Model.

    This holds the values and recommendation text.
    """

    recommendation_uuid = UUIDType()
    name = StringType()
    description = StringType()

    # Score data
    appearance = ModelType(TemplateAppearanceModel)
    sender = ModelType(TemplateSenderModel)
    relevancy = ModelType(TemplateRelevancyModel)
    behavior = ModelType(TemplateBehaviorModel)
    complexity = IntType()

    # db_tracting data added below
    created_by = StringType()
    cb_timestamp = DateTimeType()
    last_updated_by = StringType()
    lub_timestamp = DateTimeType()
