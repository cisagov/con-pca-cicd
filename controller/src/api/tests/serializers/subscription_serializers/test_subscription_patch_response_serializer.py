from api.serializers.subscriptions_serializers import (
    SubscriptionPatchResponseSerializer,
)

from datetime import datetime
from uuid import uuid4


def create(
    customer_uuid,
    name,
    url,
    keywords,
    start_date,
    gophish_campaign_list,
    primary_contact,
    status,
    target_email_list,
    templates_selected_uuid_list,
    active,
    archived,
    manually_stopped,
    created_by,
    cb_timestamp,
    last_updated_by,
    lub_timestamp,
):
    data = {
        "customer_uuid": customer_uuid,
        "name": name,
        "url": url,
        "keywords": keywords,
        "start_date": start_date,
        "gophish_campaign_list": gophish_campaign_list,
        "primary_contact": primary_contact,
        "status": status,
        "target_email_list": target_email_list,
        "templates_selected_uuid_list": templates_selected_uuid_list,
        "active": active,
        "archived": archived,
        "manually_stopped": manually_stopped,
        "created_by": created_by,
        "cb_timestamp": cb_timestamp,
        "last_updated_by": last_updated_by,
        "lub_timestamp": lub_timestamp,
    }
    serializer = SubscriptionPatchResponseSerializer(data=data)
    return serializer


def test_creation():
    customer_data = {
        "first_name": "firstname",
        "last_name": "lastname",
        "title": "sometitle",
        "office_phone": "(208)453-9032",
        "mobile_phone": "(208)453-9032",
        "email": "someemail@domain.com",
        "notes": "somenotes",
        "active": True,
    }
    target_email_list_data = {
        "first_name": "firstname",
        "last_name": "last_name",
        "email": "someemail@domain.com",
        "position": "someposition",
    }
    serializer = create(
        uuid4(),
        "name",
        "https://someurl.com",
        "keywords",
        datetime.now(),
        [],
        customer_data,
        "status",
        [target_email_list_data],
        [],
        True,
        False,
        False,
        "createdby",
        datetime.now(),
        "lastupdatedby",
        datetime.now(),
    )
    assert isinstance(serializer, SubscriptionPatchResponseSerializer)
    assert serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_missing_fields():
    customer_data = {
        "first_name": "firstname",
        "last_name": "lastname",
        "title": "sometitle",
        "office_phone": "(208)453-9032",
        "mobile_phone": "(208)453-9032",
        "email": "someemail@domain.com",
        "notes": "somenotes",
        "active": True,
    }
    target_email_list_data = {
        "first_name": "firstname",
        "last_name": "last_name",
        "email": "someemail@domain.com",
        "position": "someposition",
    }
    data = {
        "customer_uuid": uuid4(),
        # missing name field should return an invalid serializer
        "url": "https://someurl.com",
        "keywords": "keywords",
        "start_date": datetime.now(),
        "gophish_campaign_list": [],
        "primary_contact": customer_data,
        "status": "status",
        "target_email_list": [target_email_list_data],
        # missing templates_selected_uuid_list fields should not result in an error
        "active": True,
        "archived": False,
        "manually_stopped": False,
        "created_by": "createdby",
        "cb_timestamp": datetime.now(),
        "last_updated_by": "lastupdatedby",
        "lub_timestamp": datetime.now(),
    }
    serializer = SubscriptionPatchResponseSerializer(data=data)
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get("name") is not None
    assert serializer.errors.get("templates_selected_uuid_list") is None
