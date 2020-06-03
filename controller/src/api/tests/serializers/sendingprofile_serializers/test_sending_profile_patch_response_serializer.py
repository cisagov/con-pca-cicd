from api.serializers.sendingprofile_serializers import SendingProfilePatchResponseSerializer
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
    serializer = SendingProfilePatchResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.name(), fake.user_name(), fake.password(), fake.hostname(),
                        fake.word(), fake.address(), fake.boolean(), fake.date())

    assert isinstance(serializer, SendingProfilePatchResponseSerializer)
    assert serializer.is_valid()


def test_serializer_host_field_over_max_length():
    # host field over 255 characters in length should return an invalid serializer
    serializer = create(fake.random_number(), fake.name(), fake.user_name(), fake.password(), fake.random_letter()*256,
                        fake.word(), fake.address(), fake.boolean(), fake.date())

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get('host') is not None