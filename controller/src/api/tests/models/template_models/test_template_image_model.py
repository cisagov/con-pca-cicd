from api.models.template_models import TemplateImageModel

template_image_model_data = {
    "file_name": "img.jpg",
    "file_url": "localhost:8445/image.jpg",
}


def test_creation():
    tim = TemplateImageModel(template_image_model_data)
    assert isinstance(tim, TemplateImageModel)
    assert isinstance(tim.file_name, str)
    assert isinstance(tim.file_url, str)
