from api.serializers.sendingprofile_serializers import SendingProfileSerializer
from faker import Faker

fake = Faker()


def create(id, name, username, password, host, interface_type, from_address, ignore_cert_errors, modified_date):
    data = {
        'id': id,
        'name': name,
        'username': username,
        'password': password,
        'host': host,
        'interface_type': interface_type,
        'from_address': from_address,
        'ignore_cert_errors': ignore_cert_errors,
        'modified_date': modified_date
    }
    serializer = SendingProfileSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.name(), fake.user_name(), fake.password(), fake.hostname(),
                        fake.word(), fake.address(), fake.boolean(), fake.date())
    
    assert isinstance(serializer, SendingProfileSerializer)
    serializer.is_valid()
    assert len(serializer.errors) == 0