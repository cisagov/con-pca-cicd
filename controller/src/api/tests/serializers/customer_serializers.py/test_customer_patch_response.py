from api.serializers.customer_serializers import CustomerPatchResponseSerializer
from uuid import uuid4
from datetime import datetime


def test_serializer():
    data = {
        "customer_uuid": uuid4(),
        "name": "Name",
        "identifier": "id",
        "address_1": "Address",
        "address_2": "Address",
        "city": "City",
        "state": "State",
        "zip_code": "12345",
        "contact_list": [],
        "created_by": "Creator",
        "cb_timestamp": datetime(1234, 5, 6),
        "last_updated_by": "Updater",
        "lub_timestamp": datetime(9876, 4, 3),
    }
    serializer = CustomerPatchResponseSerializer(data=data)
    valid = serializer.is_valid()
    assert valid is True
