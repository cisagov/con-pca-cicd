from api.serializers.subscriptions_serializers import (
    SubscriptionDeleteResponseSerializer,
)

from uuid import uuid4


def create(subscription_uuid):
    data = {"subscription_uuid": subscription_uuid}
    serializer = SubscriptionDeleteResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(uuid4())
    assert isinstance(serializer, SubscriptionDeleteResponseSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
