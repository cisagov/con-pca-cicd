from api.serializers.customer_serializers import CustomerContactSerializer


def test_serializer():
    data = {
        "first_name": "firstname",
        "last_name": "lastname",
        "title": "title",
        "office_phone": "111-222-3333",
        "mobile_phone": "444-555-6666",
        "email": "email@email.com",
        "notes": "notes",
        "active": True,
    }

    serializer = CustomerContactSerializer(data=data)
    assert serializer.is_valid() is True


def test_serializer_null_active():
    data = {
        "first_name": "firstname",
        "last_name": "lastname",
        "title": "title",
        "office_phone": "111-222-3333",
        "mobile_phone": "444-555-6666",
        "email": "email@email.com",
        "notes": "notes",
        "active": None,
    }

    serializer = CustomerContactSerializer(data=data)
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("active") is not None
