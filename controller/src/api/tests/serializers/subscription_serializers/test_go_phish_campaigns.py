from api.serializers.subscriptions_serializers import GoPhishCampaignsSerializer
from datetime import datetime


def create(
    campaign_id,
    name,
    created_date,
    launch_date,
    send_by_date,
    completed_date,
    email_template,
    landing_page_template,
    status,
    results,
    groups,
    timeline,
    target_email_list,
):
    data = {
        "campaign_id": campaign_id,
        "name": name,
        "created_date": created_date,
        "launch_date": launch_date,
        "send_by_date": send_by_date,
        "completed_date": completed_date,
        "email_template": email_template,
        "landing_page_template": landing_page_template,
        "status": status,
        "results": results,
        "groups": groups,
        "timeline": timeline,
        "target_email_list": target_email_list,
    }
    serializer = GoPhishCampaignsSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(
        1,
        "name",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "emailtemplate",
        "landingpagetmeplate",
        "active",
        [],
        [],
        [],
        [],
    )

    assert isinstance(serializer, GoPhishCampaignsSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_fields_over_max_length():
    # name and status fields over character max length should return an invalid serializer
    serializer = create(
        1,
        "N" * 256,
        datetime.now(),
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "emailtemplate",
        "landingpagetmeplate",
        "a" * 256,
        [],
        [],
        [],
        [],
    )

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 2
    assert serializer.errors.get("name") is not None
    assert serializer.errors.get("status") is not None


def test_serializer_missing_fields():
    # missing campaign id, send by date, completed date, email template, and etc. fields should return a valid serializer since they are not required
    data = {
        "name": "name",
        "created_date": datetime.now(),
        "launch_date": datetime.now(),
        "status": "actice",
        "results": [],
        "groups": [],
        "timeline": [],
    }
    serializer = GoPhishCampaignsSerializer(data=data)

    assert serializer.is_valid()
    assert len(serializer.errors) == 0
