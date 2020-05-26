import unittest
import api.models.template_models as template_models
from database.repository.models import Model
from database.repository.types import (
    BooleanType,
    DateTimeType,
    IntType,
    ListType,
    ModelType,
    StringType,
    UUIDType,
)

class TestTemplateModels(unittest.TestCase):

    def setUp(self):
        self.appearance_model = template_models.TemplateAppearanceModel()
        self.sender_model = template_models.TemplateSenderModel()
        self.relevancy_model = template_models.TemplateRelevancyModel()
        self.behavior_model = template_models.TemplateBehaviorModel()
        self.image_model = template_models.TemplateImageModel()
        self.template_model = template_models.TemplateModel()
        

    def tearDown(self):
        pass

    def test_appearance_model_creation(self):
        self.assertIsInstance(self.appearance_model, template_models.TemplateAppearanceModel)
       
    def test_sender_model_creation(self):
        self.assertIsInstance(self.sender_model, template_models.TemplateSenderModel)

    def test_relevancy_model_creation(self):
        self.assertIsInstance(self.relevancy_model, template_models.TemplateRelevancyModel)

    def test_behavior_model_creation(self):
        self.assertIsInstance(self.behavior_model, template_models.TemplateBehaviorModel)

    def test_image_model_creation(self):
        self.assertIsInstance(self.image_model, template_models.TemplateImageModel)
    
    def test_template_model_creation(self):
        self.assertIsInstance(self.template_model, template_models.TemplateModel)