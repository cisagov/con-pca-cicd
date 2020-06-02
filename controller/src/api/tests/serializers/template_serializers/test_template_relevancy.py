from api.serializers.template_serializers import TemplateRelevancySerializer


def create(organization, public_news):
    data = {'organization': organization, 'public_news': public_news}
    serializer = TemplateRelevancySerializer(data=data)
    return serializer


def test_creation():
    serializer = create(1, 0)
    assert isinstance(serializer, TemplateRelevancySerializer)
    assert serializer.is_valid()