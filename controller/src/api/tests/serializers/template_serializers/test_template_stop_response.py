from api.serializers.template_serializers import TemplateStopResponseSerializer, TEMPLATE_TYPE_CHOICES
from uuid import uuid4
from datetime import datetime


def create(template, subscriptions):
    data = {'template': template, 'subscriptions': subscriptions}
    serializer = TemplateStopResponseSerializer(data=data)
    return serializer


def test_creation():
    image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
    appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
    sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
    relevancy_data = {'organization': 1, 'public_news': 0}
    behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
    template_patch_data = {
        'template_uuid': uuid4(),
        'gophish_template_id': 2,
        'name': 'name',
        'template_type': TEMPLATE_TYPE_CHOICES[0][0],
        'deception_score': 1,
        'descriptive_words': 'descriptive_words',
        'description': 'description',
        'image_list': [image_data],
        'from_address': 'someemail@domain.com',
        'retired': False,
        'retired_description': 'retired description',
        'subject': 'subject',
        'text': 'text',
        'html': 'html',
        'topic_list': ['topic'],
        'appearance': appearance_data,
        'sender': sender_data,
        'relevancy': relevancy_data,
        'behavior': behavior_data,
        'complexity': 2,
        'created_by': 'createdby',
        'cb_timestamp': datetime.now(),
        'last_updated_by': 'lastupdatedby',
        'lub_timestamp': datetime.now()
    }
    
    customer_data = {
        "first_name": "firstname",
        "last_name": "lastname",
        "title": "title",
        "office_phone": "111-222-3333",
        "mobile_phone": "444-555-6666",
        "email": "email@email.com",
        "notes": "notes",
        "active": True,
    }

    subscription_patch_data = {
        'customer_uuid': uuid4(),
        'name': 'name',
        'url': 'someurl.com',
        'keywords': 'keywords',
        'start_date': datetime.now(),
        'gophish_campaign_list': [],
        'primary_contact': customer_data,
        'status': 'status',
        'target_email_list': [],
        'templates_selected_uuid_list': [],
        'active': False,
        'archived': True,
        'manually_stopped': True,
        'created_by': 'createdby',
        'cb_timestamp': datetime.now(),
        'last_updated_by': 'lastupdatedby',
        'lub_timestamp': datetime.now()
    }
    serializer = create(template_patch_data, [subscription_patch_data])

    assert isinstance(serializer, TemplateStopResponseSerializer)
    assert serializer.is_valid()
    