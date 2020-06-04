from api.serializers.template_serializers import TemplatePostResponseSerializer
from faker import Faker

fake = Faker()

def create(template_uuid):
    data = {'template_uuid': template_uuid}
    serializer = TemplatePostResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.uuid4())

    assert isinstance(serializer, TemplatePostResponseSerializer)
    assert serializer.is_valid()