# Standard Libraries
from typing import Any

# Django Libraries
from django.core.management.base import BaseCommand

# Local Libraries
from notifications.views import ReportsEmailSender


class Command(BaseCommand):
    help_text = "Sends reports emails"

    def handle(self, *args: Any, **options: Any) -> None:
        message_type = "quarterly_report"
        sender = ReportsEmailSender(message_type)
        sender.send()
