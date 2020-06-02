from api.serializers.webhook_serializers import InboundWebhookSerializer
from datetime import datetime


def create(campaign_id, email, time, message, details):
    data = {
        'campaign_id': campaign_id,
        'email': email,
        'time': time,
        'message': message,
        'details': details
    }
    serializer = InboundWebhookSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(1, 'someemail@domain.com', datetime.now(), 'message', 'details')
    assert isinstance(serializer, InboundWebhookSerializer)
    assert serializer.is_valid()