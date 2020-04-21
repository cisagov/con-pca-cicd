"""
Template Serializers.

These are Django Rest Famerwork Serializers. These are used for
serializing data coming from the db into a request responce.
"""
# Third-Party Libraries
from rest_framework import serializers


class TemplateGetSerializer(serializers.Serializer):
    """
    This is the Template GET Serializer.

    This is a formats the data coming out of the Db.
    """

    template_uuid = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    system_path = serializers.CharField(max_length=200)
    deception_score = serializers.IntegerField()
    descriptive_words = serializers.DictField()
    description = serializers.CharField(max_length=200)
    display_link = serializers.CharField(max_length=200)
    from_address = serializers.CharField(max_length=200)
    retired = serializers.BooleanField()
    subject = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=200)
    topic_list = serializers.ListField()
    grammer = serializers.IntegerField()
    link_domain = serializers.IntegerField()
    logo_graphics = serializers.IntegerField()
    external = serializers.IntegerField()
    internal = serializers.IntegerField()
    authoritative = serializers.IntegerField()
    organization = serializers.IntegerField()
    public_news = serializers.IntegerField()
    fear = serializers.IntegerField()
    duty_obligation = serializers.IntegerField()
    curiosity = serializers.IntegerField()
    greed = serializers.IntegerField()
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

    name = serializers.CharField(max_length=200)
    system_path = serializers.CharField(max_length=200)
    deception_score = serializers.IntegerField()
    descriptive_words = serializers.DictField()
    description = serializers.CharField(max_length=200)
    display_link = serializers.CharField(max_length=200)
    from_address = serializers.CharField(max_length=200)
    retired = serializers.BooleanField()
    subject = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=200)
    topic_list = serializers.ListField()
    grammer = serializers.IntegerField()
    link_domain = serializers.IntegerField()
    logo_graphics = serializers.IntegerField()
    external = serializers.IntegerField()
    internal = serializers.IntegerField()
    authoritative = serializers.IntegerField()
    organization = serializers.IntegerField()
    public_news = serializers.IntegerField()
    fear = serializers.IntegerField()
    duty_obligation = serializers.IntegerField()
    curiosity = serializers.IntegerField()
    greed = serializers.IntegerField()


class TemplatePostResponseSerializer(serializers.Serializer):
    """
    This is the Template Post Response Serializer.

    This is a formats the data coming out of the Db.
    """

    template_uuid = serializers.UUIDField()
