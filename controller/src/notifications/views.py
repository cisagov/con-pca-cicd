# Standard Libraries
from typing import List

# Django Libraries
from django.core.mail.message import EmailMultiAlternatives

# Local Libraries
from notifications.utils import get_notification


class NotificationEmailSender:
    def __init__(self, recipients: List, message_type: str):
        self.recipients = recipients
        self.message_type = message_type

    def send(self):
        subject, html_path = get_notification(self.message_type)
