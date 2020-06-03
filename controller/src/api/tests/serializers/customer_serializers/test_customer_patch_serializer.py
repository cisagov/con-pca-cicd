from api.serializers.customer_serializers import CustomerPatchSerializer


def test_serializer():
    data = {
        "name": "Name",
        "identifier": "id",
        "address_1": "Address",
        "address_2": "Address",
        "city": "City",
        "state": "State",
        "zip_code": "12345",
        "contact_list": [],
    }

    serializer = CustomerPatchSerializer(data=data)

    assert serializer.is_valid() is True
