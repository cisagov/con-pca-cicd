from api.models.template_models import TemplateSenderModel

template_sender_model_data = {"external": 1, "internal": 0, "authoritative": 0}


def test_creation():
    tsm = TemplateSenderModel(template_sender_model_data)
    assert isinstance(tsm, TemplateSenderModel)
    assert isinstance(tsm.external, int)
    assert isinstance(tsm.internal, int)
    assert isinstance(tsm.authoritative, int)
