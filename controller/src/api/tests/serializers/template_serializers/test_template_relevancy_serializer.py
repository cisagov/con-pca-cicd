from api.serializers.template_serializers import TemplateRelevancySerializer
from faker import Faker

fake = Faker()

def create(organization, public_news):
    data = {'organization': organization, 'public_news': public_news}
    serializer = TemplateRelevancySerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.random_number())
    assert isinstance(serializer, TemplateRelevancySerializer)
    assert serializer.is_valid()