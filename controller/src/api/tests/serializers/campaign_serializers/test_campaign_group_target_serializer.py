from api.serializers.campaign_serializers import CampaignGroupTargetSerializer


def create(email, first_name, last_name, position):
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
    }
    serializer = CampaignGroupTargetSerializer(data=data)
    return serializer


def test_creation():
    serializer = create("someemail@domain.com", "firstname", "lastname", "someposition")
    assert isinstance(serializer, CampaignGroupTargetSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0
