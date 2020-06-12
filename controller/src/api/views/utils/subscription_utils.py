"""
Subscription Manager

This should handle subscription creation, stop and restart
for the gophish campaigns.
"""
# Standard Python Libraries
from datetime import datetime
import logging

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import (
    TagModel,
    TemplateModel,
    validate_tag,
    validate_template,
)
from api.serializers import campaign_serializers
from api.serializers.subscriptions_serializers import (
    SubscriptionDeleteResponseSerializer,
    SubscriptionGetSerializer,
    SubscriptionPatchResponseSerializer,
    SubscriptionPatchSerializer,
    SubscriptionPostResponseSerializer,
    SubscriptionPostSerializer,
)
from api.utils.db_utils import (
    delete_single,
    get_list,
    get_single,
    save_single,
    update_single,
)
from api.utils.subscription_utils import (
    get_campaign_dates,
    get_sub_end_date,
    stop_subscription,
    target_list_divide,
)
from api.utils.template_utils import format_ztime, personalize_template
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger(__name__)
# GoPhish API Manager
campaign_manager = CampaignManager()
# Template Calculator Manager
template_manager = TemplateManager()



class SubscriptionCreationManager


