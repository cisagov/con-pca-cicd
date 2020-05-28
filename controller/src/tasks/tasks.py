import os

from celery import Celery, shared_task
from celery.schedules import crontab

from config.celery import app

from api.manager import CampaignManager


campaign_manager = CampaignManager()


@shared_task
def campaign_report(campaign_id):
    """
    Pull final campaign report
    """
    campaign = campaign_manager.get("campaign", campaign_id=campaign_id)
    campaign_manager.complete_campaign(campaign_id=campaign_id)
    return campaign
