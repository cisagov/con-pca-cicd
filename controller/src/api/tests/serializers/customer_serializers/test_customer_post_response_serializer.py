from api.serializers.customer_serializers import CustomerPostResponseSerializer

from uuid import uuid4


def test_serializer():
    data = {"customer_uuid": uuid4()}
    serializer = CustomerPostResponseSerializer(data=data)
    assert serializer.is_valid() is True
