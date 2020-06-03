from api.models.template_models import TemplateAppearanceModel

template_appearance_model_data = {"grammar": 1, "link_domain": 1, "logo_graphics": 1}


def test_creation():
    tam = TemplateAppearanceModel(template_appearance_model_data)
    assert isinstance(tam, TemplateAppearanceModel)
    assert isinstance(tam.grammar, int)
    assert isinstance(tam.link_domain, int)
    assert isinstance(tam.logo_graphics, int)
