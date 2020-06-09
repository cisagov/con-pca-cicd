# Standard Libraries
from typing import List, Any

# Django Libraries
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

# Local Libraries
from notifications.utils import get_notification


class NotificationEmailSender:
    def __init__(self, recipients: List, message_type: str):
        self.recipients = recipients
        self.message_type = message_type

    def get_context_data(self, recipient):
        context: Dict[str, Any] = {}
        context["recipient"] = recipient
        return context

    def send(self):
        subject, path = get_notification(self.message_type)
        text_content = render_to_string(f"emails/{path}.txt", context)
        html_content = render_to_string(f"emails/{path}.html", context)
        for recipient in self.recipients:
            context = self.get_context_data(recipient)
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.SERVER_EMAIL,
                to=recipient,
            )
            message.attach_alternative(html_content)
            message.send(fail_silently=False)
