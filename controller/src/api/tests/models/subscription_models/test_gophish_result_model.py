from api.models.subscription_models import GoPhishResultModel
from datetime import datetime

gophish_result_model_data = {
    "first_name": "Johny",
    "last_name": "Bravo",
    "position": "CEO",
    "status": "active",
    "ip": "192.168.1.1",
    "latitude": 36.0544,
    "longitude": 112.1401,
    "send_date": datetime.now(),
    "reported": True,
}


def test_creation():
    gpr = GoPhishResultModel(gophish_result_model_data)
    assert isinstance(gpr, GoPhishResultModel) is True
