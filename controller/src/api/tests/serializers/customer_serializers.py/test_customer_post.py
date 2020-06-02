from api.serializers.customer_serializers import CustomerPostSerializer


def test_serializer():
    data = {
        "name": "name",
        "identifier": "id",
        "address_1": "123 Street",
        "address_2": "Address",
        "city": "City",
        "state": "State",
        "zip_code": "12345",
        "contact_list": [],
    }

    serializer = CustomerPostSerializer(data=data)

    assert serializer.is_valid() is True
