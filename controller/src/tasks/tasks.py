# Standard Python Libraries
import os
from datetime import timedelta

from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from celery import Celery, shared_task
from celery.schedules import crontab

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from notifications.views import ReportsEmailSender
from api.manager import CampaignManager
from api.utils.db_utils import get_single


campaign_manager = CampaignManager()


@shared_task
def email_subscription_report(subscription_uuid, message_type, send_date):
    """
    Schedule periodic subscription report emails
    """
    subscription = get_single(
        subscription_uuid, "subscription", SubscriptionModel, validate_subscription
    )

    # Send email
    sender = ReportsEmailSender(subscription, message_type)
    sender.send()

    # Schedule next task
    if message_type == "monthly_report":
        next_send_date = send_date + timedelta(days=30)
    elif message_type == "cycle_report":
        # Set GoPhish Campaign to Complete for Cycle Reports
        campaigns = subscription.get("gophish_campaign_list")
        [
            campaign_manager.complete_campaign(campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]

        # Schedule next task
        next_send_date = send_date + timedelta(days=90)
    elif message_type == "yearly_report":
        next_send_date = send_date + timedelta(days=365)

    context = {
        "subscription_uuid": subscription_uuid,
    }

    return context


@shared_task
def email_subscription_monthly(subscription):
    """
    schedule the next monthly subscription report email
    """
    # Send email
    sender = ReportsEmailSender(subscription, "monthly_report")
    sender.send()

    context = {
        "subscription_uuid": subscription.get("subscription_uuid"),
    }

    return context


@shared_task
def email_subscription_cycle(subscription):
    """
    schedule the next subscription cycle report email
    """
    # Send email
    sender = ReportsEmailSender(subscription, "cycle_report")
    sender.send()

    context = {
        "subscription_uuid": subscription.get("subscription_uuid"),
    }

    return context


@shared_task
def email_subscription_yearly(subscription):
    """
    schedule the next yearly subscription report email
    """
    # Send email
    sender = ReportsEmailSender(subscription, "yearly_report")
    sender.send()

    context = {
        "subscription_uuid": subscription.get("subscription_uuid"),
    }

    return context
