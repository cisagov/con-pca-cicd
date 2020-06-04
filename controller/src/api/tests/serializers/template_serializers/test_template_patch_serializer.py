from api.serializers.template_serializers import TemplatePatchSerializer, TEMPLATE_TYPE_CHOICES
from faker import Faker

fake = Faker()

def create(name, template_type, deception_score, descriptive_words, description, image_list,
            from_address, retired, retired_description, subject, text, html, topic_list, 
            appearance, sender, relevancy, behavior, complexity):
    
    data = {
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
        'complexity': complexity
    }
    serializer = TemplatePatchSerializer(data=data)
    return serializer


def test_creation():
    image_data = {'file_name': fake.file_name(), 'file_url': fake.image_url()}
    appearance_data = {'grammar': fake.random_number(), 'link_domain': fake.random_number(), 'logo_graphics': fake.random_number()}
    sender_data = {'external': fake.random_number(), 'internal': fake.random_number(), 'authoritative': fake.random_number()}
    relevancy_data = {'organization': fake.random_number(), 'public_news': fake.random_number()}
    behavior_data = {'fear': fake.random_number(), 'duty_obligation': fake.random_number(), 'curiosity': fake.random_number(), 'greed': fake.random_number()}
    serializer = create(fake.name(), TEMPLATE_TYPE_CHOICES[0][0], fake.random_number(), fake.word(), fake.paragraph(), [image_data], fake.email(), 
                        fake.boolean(), fake.paragraph(), fake.word(), fake.paragraph(), fake.paragraph(), [fake.word()], appearance_data, sender_data, 
                        relevancy_data, behavior_data, fake.random_number())
    
    assert isinstance(serializer, TemplatePatchSerializer)
    assert serializer.is_valid()


def test_serializer_missing_fields():
    # missing name, template type, deception score, descriptive words, description, appearance, sender, relevancy, behavior, complexity,
    # and image list fields should return a valid serializer
    data = {
        'from_address': fake.email(),
        'retired': fake.boolean(),
        'retired_description': fake.paragraph(),
        'subject': fake.word(),
        'text': fake.paragraph(),
        'html': fake.paragraph(),
        'topic_list': [fake.word()],
    }
    serializer = TemplatePatchSerializer(data=data)
    assert serializer.is_valid()