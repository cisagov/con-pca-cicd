# Standard Libraries
from typing import Any

# Django Libraries
from django.core.management.base import BaseCommand

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from notifications.views import ReportsEmailSender
from api.utils.db_utils import get_list


class Command(BaseCommand):
    help_text = "Sends reports emails"

    def handle(self, *args: Any, **options: Any) -> None:
        parameters = {"archived": {"$in": [False, None]}}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        subscription = subscription_list[0]

        message_type = "quarterly_report"
        sender = ReportsEmailSender(subscription, message_type)
        sender.send()
