from api.serializers.template_serializers import TemplateGetSerializer, TEMPLATE_TYPE_CHOICES
from uuid import uuid4
from datetime import datetime


def create(template_uuid, gophish_template_id, name, template_type, deception_score, descriptive_words,
            description, image_list, from_address, retired, retired_description, subject, text, html,
            topic_list, appearance, sender, relevancy, behavior, complexity, created_by,
            cb_timestamp, last_updated_by, lub_timestamp):
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
    serializer = TemplateGetSerializer(data = data)
    return serializer


def test_creation():
    template_image_data = {'file_name': 'img.jpg','file_url': 'someurl.com'}
    template_appearance_data = {'grammar': 1, 'link_domain': 1,  'logo_graphics': 1}
    template_sender_data = {'external': 0, 'internal': 1, 'authoritative': 1}
    template_relevancy_data = {'organization': 1, 'public_news': 0}
    template_behavior_data = { 'fear' : 1, 'duty_obligation': 1, 'curiosity': 0, 'greed': 0}

    serializer = create(uuid4(), 1, 'somename', TEMPLATE_TYPE_CHOICES[0][0], 3, 'descriptive words', 'description', [template_image_data], 'someemail@domain.com',
                        False, 'retired description', 'subject', 'text', 'html', ['topic'], template_appearance_data, template_sender_data, template_relevancy_data,
                        template_behavior_data, 1, 'createdby', datetime.now(), 'lastupdatedby', datetime.now())

    assert isinstance(serializer, TemplateGetSerializer)
    serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_fields_over_max_length():
    template_image_data = {'file_name': 'img.jpg','file_url': 'someurl.com'}
    template_appearance_data = {'grammar': 1, 'link_domain': 1,  'logo_graphics': 1}
    template_sender_data = {'external': 0, 'internal': 1, 'authoritative': 1}
    template_relevancy_data = {'organization': 1, 'public_news': 0}
    template_behavior_data = { 'fear' : 1, 'duty_obligation': 1, 'curiosity': 0, 'greed': 0}
    
    # subject, created by, and last updated by fields should return an invalid serializer if they are over the max character limit
    serializer = create(uuid4(), 1, 'somename', TEMPLATE_TYPE_CHOICES[0][0], 3, 'descriptive words', 'description', [template_image_data], 'someemail@domain.com',
                        False, 'retired description', 's'*201, 'text', 'html', ['topic'], template_appearance_data, template_sender_data, template_relevancy_data,
                        template_behavior_data, 1, 'createdby'*201, datetime.now(), 'lastupdatedby'*201, datetime.now())

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get('subject') is not None
    assert serializer.errors.get('created_by') is not None
    assert serializer.errors.get('last_updated_by') is not None
        