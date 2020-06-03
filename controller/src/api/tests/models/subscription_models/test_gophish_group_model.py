from api.models.subscription_models import GoPhishGroupModel
from api.tests.models.subscription_models.test_subscription_target_model import (
    subscription_target_model_data,
)
from datetime import datetime

gophish_group_model_data = {
    "id": 1,
    "name": "Test Group",
    "targets": [subscription_target_model_data, subscription_target_model_data],
    "modified_date": datetime.now(),
}


def test_creation():

    gpg = GoPhishGroupModel(gophish_group_model_data)
    assert isinstance(gpg, GoPhishGroupModel) is True
