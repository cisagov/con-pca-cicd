from api.serializers.sendingprofile_serializers import SendingProfilePatchSerializer
from faker import Faker

fake = Faker()


def create(name, username, password, host, interface_type, from_address, ignore_cert_errors, modified_date):
    data = {
        'name': name,
        'username': username,
        'password': password,
        'host': host,
        'interface_type': interface_type,
        'from_address': from_address,
        'ignore_cert_errors': ignore_cert_errors,
        'modified_date': modified_date
    }
    serializer = SendingProfilePatchSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.name(), fake.user_name(), fake.password(), fake.hostname(), fake.word(), fake.address(),
                        fake.boolean(), fake.date())
    
    assert isinstance(serializer, SendingProfilePatchSerializer)
    assert serializer.is_valid()


def test_serializer_missing_fields():
    # missing interface type, host, password, username, and name fields should still return a valid serializer
    data = {
        'from_address': fake.address(),
        'ignore_cert_errors': fake.boolean(),
        'modified_date': fake.date()
    }
    serializer = SendingProfilePatchSerializer(data=data)

    assert serializer.is_valid()
