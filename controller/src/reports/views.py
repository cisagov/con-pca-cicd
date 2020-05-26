import logging

# Django Libraries
from django.views.generic import TemplateView

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.utils.db_utils import get_single
from api.manager import CampaignManager
from . import views


logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()


class ReportsView(TemplateView):
    template_name = "reports/base.html"

    def get_context_data(self, **kwargs):
        subscription_uuid = self.kwargs["subscription_uuid"]
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        campaigns = subscription.get("gophish_campaign_list")
        summary = [
            campaign_manager.get("summary", campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]
        target_count = sum([targets.get("stats").get("total") for targets in summary])
        context = {
            "subscription_uuid": subscription_uuid,
            "customer_name": subscription.get("name"),
            "start_date": summary[0].get("created_date"),
            "end_date": summary[0].get("send_by_date"),
            "target_count": target_count,
        }
        return context
