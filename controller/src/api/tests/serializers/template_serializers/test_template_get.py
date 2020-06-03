from api.serializers.template_serializers import TemplateGetSerializer, TEMPLATE_TYPE_CHOICES
from faker import Faker

fake = Faker()

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
    template_image_data = {'file_name': fake.file_name(),'file_url': fake.image_url()}
    template_appearance_data = {'grammar': fake.random_number(), 'link_domain': fake.random_number(),  'logo_graphics': fake.random_number()}
    template_sender_data = {'external': fake.random_number(), 'internal': fake.random_number(), 'authoritative': fake.random_number()}
    template_relevancy_data = {'organization': fake.random_number(), 'public_news': fake.random_number()}
    template_behavior_data = { 'fear' : fake.random_number(), 'duty_obligation': fake.random_number(), 'curiosity': fake.random_number(), 'greed': fake.random_number()}

    serializer = create(fake.uuid4(), fake.random_number(), fake.name(), TEMPLATE_TYPE_CHOICES[0][0], fake.random_number(), fake.word(), fake.paragraph(), [template_image_data], fake.email(),
                        fake.boolean(), fake.paragraph(), fake.word(), fake.paragraph(), fake.paragraph(), [fake.word()], template_appearance_data, template_sender_data, template_relevancy_data,
                        template_behavior_data, fake.random_number(), fake.name(), fake.date_time(), fake.name(), fake.date_time())

    assert isinstance(serializer, TemplateGetSerializer)
    serializer.is_valid()
    assert len(serializer.errors) == 0


def test_serializer_fields_over_max_length():
    template_image_data = {'file_name': fake.file_name(),'file_url': fake.image_url()}
    template_appearance_data = {'grammar': fake.random_number(), 'link_domain': fake.random_number(),  'logo_graphics': fake.random_number()}
    template_sender_data = {'external': fake.random_number(), 'internal': fake.random_number(), 'authoritative': fake.random_number()}
    template_relevancy_data = {'organization': fake.random_number(), 'public_news': fake.random_number()}
    template_behavior_data = { 'fear' : fake.random_number(), 'duty_obligation': fake.random_number(), 'curiosity': fake.random_number(), 'greed': fake.random_number()}
    
    # subject, created by, and last updated by fields should return an invalid serializer if they are over the max character limit
    serializer = create(fake.uuid4(), fake.random_number(), fake.name(), TEMPLATE_TYPE_CHOICES[0][0], fake.random_number(), fake.word(), fake.paragraph(), [template_image_data], fake.email(),
                        fake.boolean(), fake.paragraph(), fake.random_letter()*201, fake.paragraph(), fake.paragraph(), [fake.word()], template_appearance_data, template_sender_data, template_relevancy_data,
                        template_behavior_data, fake.random_number(), fake.random_letter()*201, fake.date_time(), fake.random_letter()*201, fake.date_time())

    assert serializer.is_valid() is False
    assert len(serializer.errors) == 3
    assert serializer.errors.get('subject') is not None
    assert serializer.errors.get('created_by') is not None
    assert serializer.errors.get('last_updated_by') is not None
        