import os

from celery import Celery
from celery.schedules import crontab


# setup celery
celery = Celery('tasks', broker=os.environ.get("RABBITMQ_URL"))

# configure celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Chicago',
    enable_utc=True,
    beat_schedule={
        'example_task': {
            'task': 'src.config.example_task',
            'schedule': crontab(minute=0, hour=0),
        },
    }
)

@celery.task
def example_task():
    return 2 + 2