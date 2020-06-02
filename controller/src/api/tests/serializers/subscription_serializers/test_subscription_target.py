from api.serializers.subscriptions_serializers import SubscriptionTargetSerializer


def create(first_name, last_name, position, email):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
        "email": email,
    }
    serializer = SubscriptionTargetSerializer(data=data)
    return serializer


def test_creation():
    serializer = create("firstname", "lastname", "someposition", "fakeemail@domain.com")
    assert isinstance(serializer, SubscriptionTargetSerializer)
    assert serializer.is_valid()


def test_serializer_fields_over_max_length():
    # first name, last name, and position fields should return an invalid serializer if they are over the max character length
    serializer = create("f" * 101, "l" * 101, "p" * 101, "email@domain.com",)
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get("first_name") is not None
    assert serializer.errors.get("last_name") is not None
    assert serializer.errors.get("position") is not None
