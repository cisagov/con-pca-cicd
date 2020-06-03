from api.serializers.template_serializers import TemplateAppearanceSerializer
from faker import Faker

fake = Faker()

def create(grammar, link_domain, logo_graphics):
    data = {
        'grammar': grammar,
        'link_domain': link_domain,
        'logo_graphics': logo_graphics
    }
    serializer = TemplateAppearanceSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.random_number(), fake.random_number())
    assert serializer.is_valid()