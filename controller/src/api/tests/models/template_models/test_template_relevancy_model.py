from api.models.template_models import TemplateRelevancyModel


template_relevancy_model_data = {"organization": 1, "public_news": 1}


def test_creation():
    trm = TemplateRelevancyModel(template_relevancy_model_data)
    assert isinstance(trm, TemplateRelevancyModel)
    assert isinstance(trm.organization, int)
    assert isinstance(trm.public_news, int)
