from api.models.subscription_models import GoPhishTimelineModel
from datetime import datetime


gophish_timeline_model_data = {
    "email": "johndoe@test.com",
    "time": datetime.now(),
    "message": "Message",
    "details": "Details",
}


def test_creation():
    gpt = GoPhishTimelineModel(gophish_timeline_model_data)
    assert isinstance(gpt, GoPhishTimelineModel) is True
