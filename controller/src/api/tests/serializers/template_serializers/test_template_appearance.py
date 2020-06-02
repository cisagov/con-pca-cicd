from api.serializers.template_serializers import TemplateAppearanceSerializer


def create(grammar, link_domain, logo_graphics):
    data = {
        'grammar': grammar,
        'link_domain': link_domain,
        'logo_graphics': logo_graphics
    }
    serializer = TemplateAppearanceSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(1, 1, 1)
    assert isinstance(serializer, TemplateAppearanceSerializer)
    assert serializer.is_valid()