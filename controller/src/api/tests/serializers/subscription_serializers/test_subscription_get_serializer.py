from api.serializers.subscriptions_serializers import SubscriptionGetSerializer

from uuid import uuid4
from datetime import datetime


def create(
    subscription_uuid,
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

    data_subcritpion = {
        "subscription_uuid": subscription_uuid,
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
    serializer = SubscriptionGetSerializer(data=data_subcritpion)
    return serializer


def test_creation():
    data_customer = {
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
        uuid4(),
        "name",
        "https://www.someurl.com",
        "keywords",
        datetime.now(),
        [],
        data_customer,
        "status",
        [target_email_list_data],
        [],
        True,
        False,
        False,
        "createdby",
        datetime.now(),
        "updatedby",
        datetime.now(),
    )

    assert isinstance(serializer, SubscriptionGetSerializer)
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
    data_subcritpion = {
        "subscription_uuid": uuid4(),
        "customer_uuid": uuid4(),
        # missing url and name fields should return an invalid serializer
        "keywords": "keywords",
        "start_date": datetime.now(),
        "gophish_campaign_list": [],
        "primary_contact": customer_data,
        "status": "status",
        "target_email_list": [target_email_list_data],
        "templates_selected_uuid_list": [],
        "active": True,
        "archived": False,
        "manually_stopped": False,
        "created_by": "createdby",
        "cb_timestamp": datetime.now(),
        "last_updated_by": "lastupdatedby",
        "lub_timestamp": datetime.now(),
    }
    serializer = SubscriptionGetSerializer(data=data_subcritpion)

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 2
    assert serializer.errors.get("name") is not None
    assert serializer.errors.get("url") is not None
