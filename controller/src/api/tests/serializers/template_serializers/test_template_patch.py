from api.serializers.template_serializers import TemplatePatchSerializer, TEMPLATE_TYPE_CHOICES


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
    image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
    appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
    sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
    relevancy_data = {'organization': 1, 'public_news': 0}
    behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
    serializer = create('name', TEMPLATE_TYPE_CHOICES[0][0], 2, 'descriptive words', 'description', [image_data], 'someemail@domain.com', False, 'retired description',
                        'subject', 'text', 'html', ['topic'], appearance_data, sender_data, relevancy_data, behavior_data, 3)
    
    assert isinstance(serializer, TemplatePatchSerializer)
    assert serializer.is_valid()


def test_serializer_missing_fields():
    # missing name, template type, deception score, descriptive words, description, appearance, sender, relevancy, behavior, complexity,
    # and image list fields should return a valid serializer
    data = {
        'from_address': 'email@domain.com',
        'retired': True,
        'retired_description': 'retired description',
        'subject': 'subject',
        'text': 'text',
        'html': 'html',
        'topic_list': ['topic'],
    }
    serializer = TemplatePatchSerializer(data=data)
    assert serializer.is_valid()