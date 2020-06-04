from api.serializers.sendingprofile_serializers import SendingProfileDeleteSerializer
from faker import Faker

fake = Faker()


def create(id):
    data = {'id': id}
    serializer = SendingProfileDeleteSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number())

    assert isinstance(serializer, SendingProfileDeleteSerializer)
    assert serializer.is_valid()