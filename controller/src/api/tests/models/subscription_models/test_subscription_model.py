from api.models.subscription_models import SubscriptionModel

from api.tests.models.subscription_models.test_gophish_campaigns_model import (
    gophish_campaigns_model_data,
)
from api.tests.models.customer_models.test_customer_contact_model import (
    customer_contact_model_data,
)
from api.tests.models.subscription_models.test_subscription_target_model import (
    subscription_target_model_data,
)

import uuid
from datetime import datetime


subscription_model_data = {
    "subscription_uuid": str(uuid.uuid4()),
    "customer_uuid": str(uuid.uuid4()),
    "name": "Subscription",
    "url": "www.google.com",
    "keywords": "Test, Yes, No",
    "start_date": datetime.now(),
    "gophish_campaign_list": [
        gophish_campaigns_model_data,
        gophish_campaigns_model_data,
    ],
    "primary_contact": customer_contact_model_data,
    "status": "active",
    "target_email_list": [subscription_target_model_data],
    "templates_selected_uuid_list": [str(uuid.uuid4()), str(uuid.uuid4())],
    "active": True,
    "created_by": "Tim",
    "cb_timestamp": datetime.now(),
    "last_updated_by": "Jim",
    "lub_timestamp": datetime.now(),
}


def test_creation():
    sm = SubscriptionModel(subscription_model_data)
    assert isinstance(sm, SubscriptionModel) is True
