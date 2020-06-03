from api.serializers.template_serializers import TemplateBehaviorSerializer
from faker import Faker

fake = Faker()

def create(fear, duty_obligation, curiosity, greed):
    data = {'fear': fear, 'duty_obligation': duty_obligation, 'curiosity': curiosity, 'greed': greed}
    serializer = TemplateBehaviorSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(fake.random_number(), fake.random_number(), fake.random_number(), fake.random_number())
    assert isinstance(serializer, TemplateBehaviorSerializer)
    assert serializer.is_valid()