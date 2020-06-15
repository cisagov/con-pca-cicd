# Standard Libraries
# Standard Python Libraries
from typing import Any

# Third-Party Libraries
# Django Libraries
# Local Libraries
from django.core.management.base import BaseCommand
from notifications.views import ReportsEmailSender


class Command(BaseCommand):
    help_text = "Sends reports emails"

    def handle(self, *args: Any, **options: Any) -> None:
        recipients = ["test@example.com", "text2@example.com"]
        message_type = "quarterly_report"
        sender = ReportsEmailSender(recipients, message_type)
        sender.send()
