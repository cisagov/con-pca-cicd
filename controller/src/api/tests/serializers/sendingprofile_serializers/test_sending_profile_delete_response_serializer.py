from api.serializers.sendingprofile_serializers import SendingProfileDeleteResponseSerializer
from faker import Faker

fake = Faker()


def create(id):
    data = {'id': id}
    serializer = SendingProfileDeleteResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number())

    assert isinstance(serializer, SendingProfileDeleteResponseSerializer)
    assert serializer.is_valid()