from api.serializers.subscriptions_serializers import SubscriptionPostResponseSerializer
from uuid import uuid4


def create(subscription_uuid):
    data = {"subscription_uuid": subscription_uuid}
    serializer = SubscriptionPostResponseSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(uuid4())
    assert isinstance(serializer, SubscriptionPostResponseSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
