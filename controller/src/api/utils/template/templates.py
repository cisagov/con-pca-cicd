from api.utils import db_utils as db
from api.models.template_models import TemplateModel, validate_template

deception_level = {"high": 3, "moderate": 2, "low": 1}


def get_email_templates():
    """
    Returns a list of unretired email templates from database

    Returns:
        list: returns a list of unretired email templates
    """
    return db.get_list(
        {"template_type": "Email", "retired": False},
        "template",
        TemplateModel,
        validate_template,
    )
