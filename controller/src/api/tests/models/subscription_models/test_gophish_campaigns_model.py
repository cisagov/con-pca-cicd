from api.models.subscription_models import GoPhishCampaignsModel
from api.tests.models.subscription_models.test_gophish_result_model import (
    gophish_result_model_data,
)
from api.tests.models.subscription_models.test_gophish_group_model import (
    gophish_group_model_data,
)
from api.tests.models.subscription_models.test_gophish_timeline_model import (
    gophish_timeline_model_data,
)
from api.tests.models.subscription_models.test_subscription_target_model import (
    subscription_target_model_data,
)
from datetime import datetime


gophish_campaigns_model_data = {
    "campaign_id": 1,
    "name": "Campaign Test",
    "created_date": datetime.now(),
    "launch_date": datetime.now(),
    "send_by_date": datetime.now(),
    "completed_date": datetime.now(),
    "email_template": "Template",
    "landing_page_template": "Landing Page",
    "status": "Active",
    "results": [gophish_result_model_data, gophish_result_model_data],
    "groups": [gophish_group_model_data, gophish_group_model_data],
    "timeline": [gophish_timeline_model_data, gophish_timeline_model_data],
    "target_email_list": [
        subscription_target_model_data,
        subscription_target_model_data,
    ],
}


def test_creation():

    gpc = GoPhishCampaignsModel(gophish_campaigns_model_data)
    assert isinstance(gpc, GoPhishCampaignsModel) is True
