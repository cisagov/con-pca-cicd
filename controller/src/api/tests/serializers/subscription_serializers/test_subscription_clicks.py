from api.serializers.subscriptions_serializers import SubscriptionClicksSerializer
from datetime import datetime
from uuid import uuid4


def create(source_ip, timestamp, target_uuid):
    data = {
        "source_ip": source_ip,
        "timestamp": timestamp,
        "target_uuid": target_uuid,
    }
    serializer = SubscriptionClicksSerializer(data=data)
    return serializer


def test_creation():
    serializer = create("1.1.1.1", datetime.now(), uuid4())
    assert isinstance(serializer, SubscriptionClicksSerializer)
    assert serializer.is_valid()


def test_serializer_source_ip_field_over_max_length():
    # source ip field should return an invalid serializer if it is over the max character limit
    serializer = create(
        "1.1.54324.1231321.52432432.53253241341.5435.6.7.868768.4546.345435435.234.234.5234.22.344.1.2.3.4.5.6.7.8.8.6.54.24324.12.321.321.321",
        datetime.now(),
        uuid4(),
    )
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("source_ip") is not None
