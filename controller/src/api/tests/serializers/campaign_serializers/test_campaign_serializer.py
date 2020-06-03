from api.serializers.campaign_serializers import CampaignSerializer


def create(
    id,
    name,
    created_date,
    launch_date,
    send_by_date,
    completed_by_date,
    status,
    url,
    results,
    group,
    timeline,
):
    data = {
        "id": id,
        "name": name,
        "created_date": created_date,
        "launch_date": launch_date,
        "send_by_date": send_by_date,
        "completed_date": completed_by_date,
        "status": status,
        "url": url,
        "results": results,
        "groups": group,
        "timeline": timeline,
    }
    serializer = CampaignSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(
        1234,
        "somename",
        "2020-03-29 10:26:23.473031",
        "2020-04-29 10:26:23.473031",
        "2020-03-29 10:26:23.473031",
        "2020-03-29 10:26:23.473031",
        "active",
        "https://fakedomain.com",
        [],
        [],
        [],
    )
    assert isinstance(serializer, CampaignSerializer)
    serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_missing_name_field():
    data = {
        "id": id,
        "created_date": "2020-03-29 10:26:23.473031",
        "launch_date": "2020-03-29 10:26:23.473031",
        "send_by_date": "2020-03-29 10:26:23.473031",
        "completed_date": "2020-03-29 10:26:23.473031",
        "status": "active",
        "url": "https://fakedomain.com",
        "results": [],
        "groups": [],
        "timeline": [],
    }
    serializer = CampaignSerializer(data=data)
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("name") is not None
