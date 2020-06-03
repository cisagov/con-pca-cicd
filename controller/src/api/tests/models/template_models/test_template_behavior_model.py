from api.models.template_models import TemplateBehaviorModel

template_behavior_model_data = {
    "fear": 1,
    "duty_obligation": 1,
    "curiosity": 0,
    "greed": 0,
}


def test_creation():
    tbm = TemplateBehaviorModel(template_behavior_model_data)
    assert isinstance(tbm, TemplateBehaviorModel)
    assert isinstance(tbm.fear, int)
    assert isinstance(tbm.duty_obligation, int)
    assert isinstance(tbm.curiosity, int)
    assert isinstance(tbm.greed, int)
