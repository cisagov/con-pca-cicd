from api.serializers.template_serializers import TemplatePatchResponseSerializer, TEMPLATE_TYPE_CHOICES
from faker import Faker

fake = Faker()

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
    image_data = {'file_name': fake.file_name(), 'file_url': fake.image_url()}
    appearance_data = {'grammar': fake.random_number(), 'link_domain': fake.random_number(), 'logo_graphics': fake.random_number()}
    sender_data = {'external': fake.random_number(), 'internal': fake.random_number(), 'authoritative': fake.random_number()}
    relevancy_data = {'organization': fake.random_number(), 'public_news': fake.random_number()}
    behavior_data = {'fear': fake.random_number(), 'duty_obligation': fake.random_number(), 'curiosity': fake.random_number(), 'greed': fake.random_number()}
    serializer = create(fake.uuid4(), fake.random_number(), fake.name(), TEMPLATE_TYPE_CHOICES[0][0], fake.random_number(), fake.word(), fake.paragraph(),
                        [image_data], fake.email(), fake.boolean(), fake.paragraph(), fake.word(), fake.paragraph(),
                        fake.paragraph(), [fake.word()], appearance_data, sender_data, relevancy_data, behavior_data, fake.random_number(), fake.name(),
                        fake.date_time(), fake.name(), fake.date_time())
    
    assert isinstance(serializer, TemplatePatchResponseSerializer)
    assert serializer.is_valid()


def test_serializer_fields_over_max_length():
    # subject, created by, and last updated by fields over 200 characters should return an invalid serializer
    image_data = {'file_name': fake.file_name(), 'file_url': fake.image_url()}
    appearance_data = {'grammar': fake.random_number(), 'link_domain': fake.random_number(), 'logo_graphics': fake.random_number()}
    sender_data = {'external': fake.random_number(), 'internal': fake.random_number(), 'authoritative': fake.random_number()}
    relevancy_data = {'organization': fake.random_number(), 'public_news': fake.random_number()}
    behavior_data = {'fear': fake.random_number(), 'duty_obligation': fake.random_number(), 'curiosity': fake.random_number(), 'greed': fake.random_number()}
    serializer = create(fake.uuid4(), fake.random_number(), fake.name(), TEMPLATE_TYPE_CHOICES[0][0], fake.random_number(), fake.word(), fake.paragraph(),
                        [image_data], fake.email(), fake.boolean(), fake.paragraph(), fake.random_letter()*201, fake.paragraph(),
                        fake.paragraph(), [fake.word()], appearance_data, sender_data, relevancy_data, behavior_data, fake.random_number(), fake.random_letter()*201,
                        fake.date_time(), fake.random_letter()*201, fake.date_time())

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get('subject') is not None
    assert serializer.errors.get('created_by') is not None
    assert serializer.errors.get('last_updated_by') is not None
