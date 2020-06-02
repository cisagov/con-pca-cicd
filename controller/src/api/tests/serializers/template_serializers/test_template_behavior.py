from api.serializers.template_serializers import TemplateBehaviorSerializer


def create(fear, duty_obligation, curiosity, greed):
    data = {'fear': fear, 'duty_obligation': duty_obligation, 'curiosity': curiosity, 'greed': greed}
    serializer = TemplateBehaviorSerializer(data=data)
    return serializer


def test_creation():
    serializer = create(1, 1, 0, 0)
    assert isinstance(serializer, TemplateBehaviorSerializer)
    assert serializer.is_valid()