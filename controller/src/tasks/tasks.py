# Standard Python Libraries
import os

# Third-Party Libraries
# Local Libraries
# Third Party Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from celery import Celery, shared_task
from celery.schedules import crontab
from config.celery import app

campaign_manager = CampaignManager()


@shared_task
def subscription_report(subscription_uuid):
    """
    Pull final subscription report
    """
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
    # Set Subscription's Active task to True
    subscription["active_task"] = True
    # Set GoPhish Campaign to Complete
    campaign_manager.complete_campaign(campaign_id=campaign_id)

    return context
