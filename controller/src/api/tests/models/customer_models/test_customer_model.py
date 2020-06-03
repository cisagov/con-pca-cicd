from api.models.customer_models import CustomerModel
from uuid import uuid4
from datetime import datetime


customer_model_data = {
    "customer_uuid": str(uuid4()),
    "name": "McDonalds",
    "identifier": "id",
    "address_1": "123 Street",
    "address_2": "#3",
    "city": "City",
    "state": "State",
    "zip_code": "12345",
    "contact_list": [],
    "created_by": "Creator",
    "cb_timestamp": datetime(1234, 5, 6),
    "last_updated_by": "Updater",
    "lub_timestamp": datetime(7890, 1, 2),
}


def test_creation():
    c = CustomerModel(customer_model_data)
    assert isinstance(c, CustomerModel) is True
