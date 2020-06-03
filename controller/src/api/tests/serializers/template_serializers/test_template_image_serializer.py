from api.serializers.template_serializers import TemplateImageSerializer
from faker import Faker

fake = Faker()

def create(file_name, file_url):
    data = {'file_name': file_name, 'file_url': file_url}
    serializer = TemplateImageSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.file_name(), fake.image_url())
    assert isinstance(serializer, TemplateImageSerializer)
    assert serializer.is_valid()