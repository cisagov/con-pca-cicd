from api.serializers.template_serializers import TemplateImageSerializer


def create(file_name, file_url):
    data = {'file_name': file_name, 'file_url': file_url}
    serializer = TemplateImageSerializer(data=data)
    return serializer


def test_creation():
    serializer = create('someimage.jpg', 'someurl.com')
    assert isinstance(serializer, TemplateImageSerializer)
    assert serializer.is_valid()