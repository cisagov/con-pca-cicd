from uuid import uuid4
from datetime import datetime

from api.serializers.customer_serializers import CustomerGetSerializer


def test_serializer():
    data = {
        "customer_uuid": uuid4(),
        "name": "JimmyJohns",
        "identifier": "id",
        "address_1": "123 Street Street",
        "address_2": "456 Road Way",
        "city": "Citysburg",
        "state": "New Kansas",
        "zip_code": "12345",
        "contact_list": [],
        "created_by": "creator",
        "cb_timestamp": datetime(1234, 5, 6),
        "last_updated_by": "Updater",
        "lub_timestamp": datetime(9876, 5, 4),
    }
    serializer = CustomerGetSerializer(data=data)
    assert serializer.is_valid() is True
