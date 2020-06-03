from api.serializers.template_serializers import TemplatePatchResponseSerializer, TEMPLATE_TYPE_CHOICES
from uuid import uuid4
from datetime import datetime

def create(template_uuid, gophish_template_id, name, template_type, deception_score, descriptive_words,
            description, image_list, from_address, retired, retired_description, subject, text, html,
            topic_list, appearance, sender, relevancy, behavior, complexity, created_by, cb_timestamp,
            last_updated_by, lub_timestamp):

    data = {
        'template_uuid': template_uuid,
        'gophish_template_id': gophish_template_id,
        'name': name,
        'template_type': template_type,
        'deception_score': deception_score,
        'descriptive_words': descriptive_words,
        'description': description,
        'image_list': image_list,
        'from_address': from_address,
        'retired': retired,
        'retired_description': retired_description,
        'subject': subject,
        'text': text,
        'html': html,
        'topic_list': topic_list,
        'appearance': appearance,
        'sender': sender,
        'relevancy': relevancy,
        'behavior': behavior,
        'complexity': complexity,
        'created_by': created_by,
        'cb_timestamp': cb_timestamp,
        'last_updated_by': last_updated_by,
        'lub_timestamp': lub_timestamp
    }
    serializer = TemplatePatchResponseSerializer(data=data)
    return serializer


def test_creation():
    image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
    appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
    sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
    relevancy_data = {'organization': 1, 'public_news': 0}
    behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
    serializer = create(uuid4(), 2, 'name', TEMPLATE_TYPE_CHOICES[0][0], 2, 'descriptive words', 'description',
                        [image_data], 'someemail@domain.com', False, 'retired description', 'subject', 'text',
                        'html', ['topic'], appearance_data, sender_data, relevancy_data, behavior_data, 3, 'createdby', datetime.now(),
                        'lastupdatedby', datetime.now())
    
    assert isinstance(serializer, TemplatePatchResponseSerializer)
    assert serializer.is_valid()


def test_serializer_fields_over_max_length():
    # subject, created by, and last updated by fields over 200 characters should return an invalid serializer
    image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
    appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
    sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
    relevancy_data = {'organization': 1, 'public_news': 0}
    behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
    serializer = create(uuid4(), 2, 'name', TEMPLATE_TYPE_CHOICES[0][0], 2, 'descriptive words', 'description',
                        [image_data], 'someemail@domain.com', False, 'retired description', 's'*201, 'text',
                        'html', ['topic'], appearance_data, sender_data, relevancy_data, behavior_data, 3, 'c'*201, datetime.now(),
                        'l'*201, datetime.now())

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get('subject') is not None
    assert serializer.errors.get('created_by') is not None
    assert serializer.errors.get('last_updated_by') is not None
