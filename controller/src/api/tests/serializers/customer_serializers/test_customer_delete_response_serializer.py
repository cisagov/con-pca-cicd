from api.serializers.customer_serializers import CustomerDeleteResponseSerializer
from uuid import uuid4


def test_serializer():
    data = {"customer_uuid": uuid4()}
    assert CustomerDeleteResponseSerializer(data=data).is_valid() is True
