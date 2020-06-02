from api.serializers.campaign_serializers import CampaignEventSerializer

def create(email, time, message, details):
        data = {"email": email, "time": time, "message": message, "details": details}
        serializer = CampaignEventSerializer(data=data)
        return serializer

def test_creation():
    serializer = create(
        "someemail@domain.com",
        "2020-03-29 10:26:23.473031",
        "some test message",
        "some test details",
    )
    assert isinstance(serializer, CampaignEventSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0