from api.serializers.subscriptions_serializers import GoPhishTimelineSerializer

from datetime import datetime


def create(email, time, message, details):
    data = {"email": email, "time": time, "message": message, "details": details}
    serializer = GoPhishTimelineSerializer(data=data)
    return serializer


def test_creation():
    serializer = create("email@domain.com", datetime.now(), "message", "details")

    assert isinstance(serializer, GoPhishTimelineSerializer)
    assert serializer.is_valid()


def test_serializer_missing_email_field():
    # missing email field should return a valid serializer
    data = {"time": datetime.now(), "message": "message", "details": "details"}
    serializer = GoPhishTimelineSerializer(data=data)

    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("email") is None


def test_serializer_message_field_over_max_length():
    # message field over max character length should return an invalid serializer
    serializer = create("email@domain.com", datetime.now(), "f" * 256, "details",)

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("message") is not None
