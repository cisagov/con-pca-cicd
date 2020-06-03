from api.models.subscription_models import SubscriptionTargetModel

subscription_target_model_data = {
    "first_name": "Johnny",
    "last_name": "Bravo",
    "position": "CEO",
    "email": "johnny.bravo@test.com",
}


def test_creation():
    st = SubscriptionTargetModel(subscription_target_model_data)
    assert isinstance(st, SubscriptionTargetModel) is True
