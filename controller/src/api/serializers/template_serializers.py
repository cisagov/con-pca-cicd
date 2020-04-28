"""
Template Serializers.

These are Django Rest Famerwork Serializers. These are used for
serializing data coming from the db into a request responce.
"""
# Third-Party Libraries
from rest_framework import serializers


class TemplateAppearanceSerializer(serializers.Serializer):
    """
    This is the Template Serializer.

    This holds values for template Appearance Score.
    """

    grammar = serializers.IntegerField()
    link_domain = serializers.IntegerField()
    logo_graphics = serializers.IntegerField()


class TemplateSenderSerializer(serializers.Serializer):
    """
    This is the Template Sender Serializer.

    This holds values for template Sender Score.
    """

    external = serializers.IntegerField()
    internal = serializers.IntegerField()
    authoritative = serializers.IntegerField()


class TemplateRelevancySerializer(serializers.Serializer):
    """
    This is the Template Relevancy Serializer.

    This holds values for template Relevancy Score.
    """

    organization = serializers.IntegerField()
    public_news = serializers.IntegerField()


class TemplateBehaviorSerializer(serializers.Serializer):
    """
    This is the Template Behavior Model.

    This holds values for template Behavior Score.
    """

    fear = serializers.IntegerField()
    duty_obligation = serializers.IntegerField()
    curiosity = serializers.IntegerField()
    greed = serializers.IntegerField()


class TemplateGetSerializer(serializers.Serializer):
    """
    This is the Template GET Serializer.

    This is a formats the data coming out of the Db.
    """

    template_uuid = serializers.UUIDField()
    name = serializers.CharField()
    deception_score = serializers.IntegerField()
    descriptive_words = serializers.DictField()
    description = serializers.CharField()
    display_link = serializers.CharField(max_length=200)
    from_address = serializers.EmailField()
    retired = serializers.BooleanField()
    subject = serializers.CharField(max_length=200)
    text = serializers.CharField()
    topic_list = serializers.ListField()
    # Score data
    appearance = TemplateAppearanceSerializer()
    sender = TemplateSenderSerializer()
    relevancy = TemplateRelevancySerializer()
    behavior = TemplateBehaviorSerializer()
    complexity = serializers.IntegerField()
    # db_tracting data added below
    created_by = serializers.CharField(max_length=200)
    cb_timestamp = serializers.DateTimeField()
    last_updated_by = serializers.CharField(max_length=200)
    lub_timestamp = serializers.DateTimeField()


class TemplatePostSerializer(serializers.Serializer):
    """
    This is the Template GET Serializer.

    This is a formats the data coming out of the Db.
    """

    name = serializers.CharField()
    deception_score = serializers.IntegerField()
    descriptive_words = serializers.DictField()
    description = serializers.CharField()
    display_link = serializers.CharField(max_length=200)
    from_address = serializers.EmailField()
    retired = serializers.BooleanField()
    subject = serializers.CharField(max_length=200)
    text = serializers.CharField()
    topic_list = serializers.ListField()
    # Score data
    appearance = TemplateAppearanceSerializer()
    sender = TemplateSenderSerializer()
    relevancy = TemplateRelevancySerializer()
    behavior = TemplateBehaviorSerializer()
    complexity = serializers.IntegerField()


class TemplatePostResponseSerializer(serializers.Serializer):
    """
    This is the Template Post Response Serializer.

    This is a formats the data coming out of the Db.
    """

    template_uuid = serializers.UUIDField()
