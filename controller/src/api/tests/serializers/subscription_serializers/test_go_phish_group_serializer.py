from datetime import datetime

from api.serializers.subscriptions_serializers import GoPhishGroupSerializer


def create(id, name, targets, modified_date):
    data = {
        "id": id,
        "name": name,
        "targets": targets,
        "modified_date": modified_date,
    }
    serializer = GoPhishGroupSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(1, "name", [], datetime.now())

    assert isinstance(serializer, GoPhishGroupSerializer)
    assert serializer.is_valid()


def test_serializer_missing_id_field():
    # missing id field should return a valid serializer since it is not required
    data = {"name": "name", "targets": [], "modified_date": datetime.now()}
    serializer = GoPhishGroupSerializer(data=data)

    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("id") is None


def test_serializer_name_field_over_max_length():
    # name field over max character length should return an invalid serializer
    serializer = create(1, "n" * 256, [], datetime.now(),)

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("name") is not None
