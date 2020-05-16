import os

from celery import Celery, shared_task
from celery.schedules import crontab

from config.celery import app


@shared_task
def campaign_report(word):
    """
    Pull final campaign report
    """
    print(word)
    return word
