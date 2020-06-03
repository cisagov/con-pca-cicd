from api.serializers.template_serializers import TemplatePostResponseSerializer
from uuid import uuid4


def create(template_uuid):
    data = {'template_uuid': template_uuid}
    serializer = TemplatePostResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(uuid4())

    assert isinstance(serializer, TemplatePostResponseSerializer)
    assert serializer.is_valid()