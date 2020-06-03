from api.serializers.subscriptions_serializers import GoPhishResultSerializer
from datetime import datetime


def create(
    id,
    first_name,
    last_name,
    position,
    status,
    ip,
    latitude,
    longitude,
    send_date,
    reported,
):
    data = {
        "id": id,
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
        "status": status,
        "ip": ip,
        "latitude": latitude,
        "longitude": longitude,
        "send_date": send_date,
        "reported": reported,
    }
    serializer = GoPhishResultSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(
        1,
        "firstname",
        "lastname",
        "position",
        "active",
        "1.1.1.1",
        38.9432,
        -77.8951,
        datetime.now(),
        True,
    )
    assert isinstance(serializer, GoPhishResultSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_fields_over_max_length():
    # first name, last name, and status fields should return an invalid serializer if thet are over the max character limit
    serializer = create(
        1,
        "f" * 256,
        "l" * 256,
        "postion",
        "s" * 256,
        "1.1.1.1",
        38.9432,
        -77.8951,
        datetime.now(),
        True,
    )
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get("first_name") is not None
    assert serializer.errors.get("last_name") is not None
    assert serializer.errors.get("status") is not None


def test_serializer_missing_send_date_field():
    # missing send date field should return a valid serializer
    data = {
        "id": 1,
        "first_name": "firstname",
        "last_name": "lastname",
        "position": "position",
        "status": "status",
        "ip": "1.1.1.1",
        "latitude": -77.8951,
        "longitude": 38.9432,
        "reported": True,
    }
    serializer = GoPhishResultSerializer(data=data)

    assert serializer.is_valid() is True
    assert len(serializer.errors) == 0
    assert serializer.errors.get("send_date") is None
