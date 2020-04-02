import os

from celery import Celery, shared_task
from celery.schedules import crontab


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
