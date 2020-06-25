"""Tempalte Utils."""
# Third-Party Libraries
from api.models.template_models import (
    TargetHistoryModel,
    TemplateModel,
    validate_history,
    validate_template,
)
from api.utils import db_utils as db

deception_level = {"high": 3, "moderate": 2, "low": 1}


def get_email_templates():
    """
    Returns a list of unretired email templates from database.

    Returns:
        list: returns a list of unretired email templates
    """
    return db.get_list(
        {"template_type": "Email", "retired": False},
        "template",
        TemplateModel,
        validate_template,
    )


def update_target_history(campaign_info, target_email):
    """Update target History.

    Args:
        campaign_info (dict): campaign_info
        target_email (string): target_email
    """
    # check if email target exists, if not, create
    document_list = db.get_list(
        {"email": target_email}, "target", TargetHistoryModel, validate_history
    )
    if document_list:
        # get object and update
        print("get object and update")
        print(document_list[0])
    else:
        # create new
        print("create new target history")

    return
