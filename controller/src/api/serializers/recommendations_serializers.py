"""
Recommendation Serializers.

These are Django Rest Framework Serializers. These are used for
serializing data coming from the db into a request response.
"""
# Third-Party Libraries
from rest_framework import serializers

from api.serializers.template_serializers import (
    TemplateAppearanceSerializer,
    TemplateSenderSerializer,
    TemplateRelevancySerializer,
    TemplateBehaviorSerializer,
)


class RecommendationsGetSerializer(serializers.Serializer):
    """
    This is the Recommendation GET Serializer.

    This is a formats the data coming out of the Db.
    """

    recommendations_uuid = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    # Score data
    appearance = TemplateAppearanceSerializer()
    sender = TemplateSenderSerializer()
    relevancy = TemplateRelevancySerializer()
    behavior = TemplateBehaviorSerializer()
    complexity = serializers.IntegerField()
    # db tracking data added below
    created_by = serializers.CharField(max_length=200)
    cb_timestamp = serializers.DateTimeField()
    last_updated_by = serializers.CharField(max_length=200)
    lub_timestamp = serializers.DateTimeField()


class RecommendationsPostSerializer(serializers.Serializer):
    """
    This is the Recommendation POST Serializer.

    This is a formats the data coming out of the Db.
    """

    name = serializers.CharField()
    description = serializers.CharField()
    # Score data
    appearance = TemplateAppearanceSerializer()
    sender = TemplateSenderSerializer()
    relevancy = TemplateRelevancySerializer()
    behavior = TemplateBehaviorSerializer()
    complexity = serializers.IntegerField()


class RecommendationsPostResponseSerializer(serializers.Serializer):
    """
    This is the Recommendation Post Response Serializer.

    This is a formats the data coming out of the Db.
    """

    recommendations_uuid = serializers.UUIDField()


class RecommendationsQuerySerializer(serializers.Serializer):
    """
    Serializes Recommendations Query.

    This is sets queries we can run on db collection.
    """

    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    complexity = serializers.IntegerField(required=False)
    created_by = serializers.CharField(required=False)
    cb_timestamp = serializers.DateTimeField(required=False)
    last_updated_by = serializers.CharField(required=False)
    lub_timestamp = serializers.DateTimeField(required=False)
