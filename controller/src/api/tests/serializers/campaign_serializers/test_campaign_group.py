from api.serializers.campaign_serializers import CampaignGroupSerializer

def create(id, name, targets, modified_date):
        data = {
            "id": id,
            "name": name,
            "targets": targets,
            "modified_date": modified_date,
        }
        serializer = CampaignGroupSerializer(data=data)
        return serializer

def test_creation():
    serializer = create(12943, "somename", [], "2020-03-29 10:26:23.473031")
    assert isinstance(serializer, CampaignGroupSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("name") is None

def test_serializer_missing_name_field():
    data = {"id": id, "targets": [], "modified_date": "2020-03-29 10:26:23.473031"}
    serializer = CampaignGroupSerializer(data=data)

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("name") is not None
