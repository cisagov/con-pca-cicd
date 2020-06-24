# Standard Python Libraries
import os

from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from celery import Celery, shared_task
from celery.schedules import crontab
from config.celery import app

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from notifications.views import ReportsEmailSender
from api.manager import CampaignManager
from api.utils.db_utils import get_single


campaign_manager = CampaignManager()


@shared_task
def email_subscription_report(subscription_uuid, message_type):
    """
    Pull final subscription report
    """
    subscription = get_single(
        subscription_uuid, "subscription", SubscriptionModel, validate_subscription
    )

    # Send email
    sender = ReportsEmailSender(subscription, message_type)
    sender.send()

    # Set GoPhish Campaign to Complete for Cycle Reports
    if message_type == "cycle_report":
        campaigns = subscription.get("gophish_campaign_list")
        [
            campaign_manager.complete_campaign(campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]

    context = {
        "subscription_uuid": subscription_uuid,
    }

    return context
