from api.serializers.template_serializers import TemplateSenderSerializer
from faker import Faker

fake = Faker()

def create(external, internal, authoritative):
    data = {
        'external': external,
        'internal': internal,
        'authoritative': authoritative
    }
    serializer = TemplateSenderSerializer(data = data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.random_number(), fake.random_number())
    assert isinstance(serializer, TemplateSenderSerializer)
    assert serializer.is_valid()