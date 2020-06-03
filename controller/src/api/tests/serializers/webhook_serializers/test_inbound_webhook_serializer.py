from api.serializers.webhook_serializers import InboundWebhookSerializer
from faker import Faker

fake = Faker()

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
    serializer = create(fake.random_number(), fake.email(), fake.date_time(), fake.paragraph(), fake.paragraph())
    assert isinstance(serializer, InboundWebhookSerializer)
    serializer.is_valid()
    assert len(serializer.errors) == 0