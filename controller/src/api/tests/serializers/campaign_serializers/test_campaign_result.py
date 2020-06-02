from api.serializers.campaign_serializers import CampaignResultSerializer


def create(
    id,
    first_name,
    last_name,
    position,
    status,
    ip,
    latitude,
    longitude,
    send_date,
    reported,
):
    data = {
        "id": id,
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
        "status": status,
        "ip": ip,
        "latitude": latitude,
        "longitude": longitude,
        "send_date": send_date,
        "reported": reported,
    }
    serilaizer = CampaignResultSerializer(data=data)
    return serilaizer


def test_creation():
    serializer = create(
        "12345",
        "firstname",
        "lastname",
        "someposition",
        "inactive",
        "1.1.1.1",
        38.9432,
        -77.8951,
        "2020-03-29 10:26:23.473031",
        True,
    )
    assert isinstance(serializer, CampaignResultSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("active") is None


def test_serializer_missing_reported_field():
    data = {
        "id": 12345,
        "first_name": "firstname",
        "last_name": "lastname",
        "position": "someposition",
        "status": "inactive",
        "ip": "1.1.1.1",
        "latitude": 38.9432,
        "longitude": -77.8951,
        "send_date": "2020-03-29 10:26:23.473031",
    }
    serializer = CampaignResultSerializer(data=data)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("reported") is None


def test_serializer_missing_send_date_field():
    data = {
        "id": 12345,
        "first_name": "firstname",
        "last_name": "lastname",
        "position": "someposition",
        "status": "inactive",
        "ip": "1.1.1.1",
        "latitude": 38.9432,
        "longitude": -77.8951,
        "reported": False,
    }
    serializer = CampaignResultSerializer(data=data)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.errors.get("send_date") is None
