from api.serializers.template_serializers import TemplateSenderSerializer


def create(external, internal, authoritative):
    data = {
        'external': external,
        'internal': internal,
        'authoritative': authoritative
    }
    serializer = TemplateSenderSerializer(data = data)
    return serializer


def test_creation():
    serializer = create(1, 0, 1)
    assert isinstance(serializer, TemplateSenderSerializer)
    assert serializer.is_valid()