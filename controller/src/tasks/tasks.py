import os

# Third Party Libraries
from celery import Celery, shared_task
from celery.schedules import crontab
from config.celery import app

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from notifications.views import ReportsEmailSender
from api.manager import CampaignManager


campaign_manager = CampaignManager()


@shared_task
def email_subscription_report(subscription_uuid, message_type):
    """
    Pull final subscription report
    """
    subscription = get_single(
        subscription_uuid, "subscription", SubscriptionModel, validate_subscription
    )
    campaigns = subscription.get("gophish_campaign_list")

    # Send email
    sender = ReportsEmailSender(subscription, message_type)
    sender.send()

    # Set Subscription's Active task to True
    subscription["active_task"] = True

    # Set GoPhish Campaign to Complete
    [
        campaign_manager.complete_campaign(campaign_id=campaign_id)
        for campaign in campaigns
    ]

    context = {
        "subscription_uuid": subscription_uuid,
    }

    return context
