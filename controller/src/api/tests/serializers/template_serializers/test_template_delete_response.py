from api.serializers.template_serializers import TemplateDeleteResponseSerializer
from uuid import uuid4


def create(template_uuid):
    data = {'template_uuid': template_uuid}
    serializer = TemplateDeleteResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(uuid4())

    assert isinstance(serializer, TemplateDeleteResponseSerializer)
    assert serializer.is_valid()