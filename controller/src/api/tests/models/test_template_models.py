import pytest
import api.models.template_models as tm
import datetime
import uuid
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

class TestTemplateAppearanceModel:
    
    def create(self, grammar = 1, link_domain = 1, logo_graphics = 1):
        template_appearance_model = tm.TemplateAppearanceModel()
        template_appearance_model.grammar = grammar
        template_appearance_model.link_domain = link_domain
        template_appearance_model.logo_graphics = logo_graphics
        return template_appearance_model

    def test_creation(self):
        tam = self.create()
        assert isinstance(tam, tm.TemplateAppearanceModel) 

class TestTemplateSenderModel:
    
    def create(self, external = 1, internal = 0, authoritative = 0):
        template_sender_model = tm.TemplateSenderModel()
        template_sender_model.external = external
        template_sender_model.internal = internal
        template_sender_model.authoritative = authoritative
        return template_sender_model

    def test_creation(self):
        tsm = self.create()
        assert isinstance(tsm, tm.TemplateSenderModel) 

class TestTemplateRelevancyModel:
    
    def create(self, organization = 1, public_news = 1):
        template_relevancy_model = tm.TemplateRelevancyModel()
        template_relevancy_model.organization = organization
        template_relevancy_model.public_news = public_news
        return template_relevancy_model

    def test_creation(self):
        trm = self.create()
        assert isinstance(trm, tm.TemplateRelevancyModel) 

class TestTemplateBehaviorModel:
    
    def create(self, fear = 1, duty_obligation = 1, curiosity = 0, greed = 0):
        template_behavior_model = tm.TemplateBehaviorModel()
        template_behavior_model.fear = fear
        template_behavior_model.duty_obligation = duty_obligation
        template_behavior_model.curiosity = curiosity
        template_behavior_model.greed = greed
        return template_behavior_model

    def test_creation(self):
        tbm = self.create()
        assert isinstance(tbm, tm.TemplateBehaviorModel)

class TestTemplateImageModel:
    
    def create(self, file_name = "img.jpg", file_url = "https://fakeurl.com"):
        template_image_model = tm.TemplateImageModel()
        template_image_model.file_name = file_name
        template_image_model.file_url = file_url
        return template_image_model

    def test_creation(self):
        tim = self.create()
        assert isinstance(tim, tm.TemplateImageModel)

class TestTemplateModel:
    
    def create(self, template_uuid = str(uuid.uuid4()), gophish_template_id = 12942, name = "Test", template_type = "test template", deception_score = 2, 
                descriptive_words = "test", description = "This is a test", image_list = [tm.TemplateImageModel()], from_address = "spoof address", 
                retired = False, retired_description = "N/A", subject = "spoof email", text = "text", html = "html", topic_list = ["topic 1", "topic 2"],
                appearance = tm.TemplateAppearanceModel(), sender = tm.TemplateSenderModel(), relavancy = tm.TemplateRelevancyModel(), 
                behavior = tm.TemplateBehaviorModel(), complexity = 5, created_by = "creator", cb_timestamp = datetime.datetime.now(), last_updated_by = "updater",
                lub_timestamp = datetime.datetime.now()):
        template_model = tm.TemplateModel()
        template_model.template_uuid = template_uuid
        template_model.gophish_template_id = gophish_template_id
        template_model.name = name
        template_model.template_type = template_type
        template_model.deception_score = deception_score
        template_model.descriptive_words = descriptive_words
        template_model.description = description
        template_model.image_list = image_list
        template_model.from_address = from_address
        template_model.retired = retired
        template_model.retired_description = retired_description
        template_model.subject = subject
        template_model.text = text
        template_model.html = html
        template_model.topic_list = topic_list
        template_model.appearance = appearance
        template_model.sender = sender 
        template_model.relevancy = relavancy
        template_model.behavior = behavior
        template_model.complexity = complexity
        template_model.created_by = created_by
        template_model.cb_timestamp = cb_timestamp
        template_model.last_updated_by = last_updated_by
        template_model.lub_timestamp = lub_timestamp
        return template_model

    def test_creation(self):
        template_model = self.create()
        assert isinstance(template_model, tm.TemplateModel)
        
class TestValidateTemplate:

    def test_validate_template(self):
        test_model = TestTemplateModel()
        data_object = test_model.create()
        tm.validate_template(data_object)