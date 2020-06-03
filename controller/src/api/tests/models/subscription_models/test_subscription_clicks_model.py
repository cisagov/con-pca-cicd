from api.models.subscription_models import SubscriptionClicksModel
from datetime import datetime
import uuid

subscription_clicks_model_data = {
    "source_ip": "192.168.1.1",
    "timestamp": datetime.now(),
    "target_uuid": str(uuid.uuid4()),
}


def test_creation():
    sc = SubscriptionClicksModel(subscription_clicks_model_data)
    assert isinstance(sc, SubscriptionClicksModel) is True
