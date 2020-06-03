from api.serializers.template_serializers import TemplatePostSerializer, TEMPLATE_TYPE_CHOICES


def create(gophish_template_id, name, template_type, deception_score, descriptive_words, description, image_list, from_address, retired, retired_description, subject,
            text, html, topic_list, appearance, sender, relevancy, behavior, complexity):
    data = {
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
        'complexity': complexity
    }
    serializer = TemplatePostSerializer(data=data)
    return serializer

def test_creation():
        image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
        appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
        sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
        relevancy_data = {'organization': 1, 'public_news': 0}
        behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
        serializer = create(1, 'name', TEMPLATE_TYPE_CHOICES[0][0], 2, 'descriptive words', 'description', [image_data], 'someemail@domain.com', False, 'retired description',
                            'subject', 'text', 'html', ['topic'], appearance_data, sender_data, relevancy_data, behavior_data, 3)

        assert isinstance(serializer, TemplatePostSerializer)
        serializer.is_valid()
        assert len(serializer.errors) == 0

def test_serializer_subject_field_over_max_length():
    # subject field over 200 characters should return an invalid serializer
    image_data = {'file_name': 'img.jpg', 'file_url': 'someurl.com'}
    appearance_data = {'grammar': 1, 'link_domain': 1, 'logo_graphics': 1}
    sender_data = {'external': 1, 'internal': 0, 'authoritative': 1}
    relevancy_data = {'organization': 1, 'public_news': 0}
    behavior_data = {'fear': 1, 'duty_obligation': 0, 'curiosity': 0, 'greed': 0}
    serializer = create(1, 'name', TEMPLATE_TYPE_CHOICES[0][0], 2, 'descriptive words', 'description', [image_data], 'someemail@domain.com', False, 'retired description',
                        's'*201, 'text', 'html', ['topic'], appearance_data, sender_data, relevancy_data, behavior_data, 3)
    
    assert serializer.is_valid() is False
    assert len(serializer.errors) == 1
    assert serializer.errors.get('subject') is not None
