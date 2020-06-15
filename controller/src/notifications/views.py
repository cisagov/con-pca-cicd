# Standard Libraries
# Standard Python Libraries
from typing import Any, List

# Third-Party Libraries
# Django Libraries
# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.utils.db_utils import get_list
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from notifications.utils import get_notification
from weasyprint import HTML


class ReportsEmailSender:
    def __init__(self, recipients: List, message_type: str):
        self.recipients = recipients
        self.message_type = message_type

    def get_context_data(self, recipient):
        context: Dict[str, Any] = {}
        context["recipient"] = recipient
        return context

    def get_attachment(self, subscription_uuid):
        html = HTML(f"http://localhost:8000/reports/{subscription_uuid}/")
        html.write_pdf("/tmp/subscription_report.pdf")

        fs = FileSystemStorage("/tmp")
        return fs.open("subscription_report.pdf")

    def send(self):
        subject, path = get_notification(self.message_type)
        # get subscription
        parameters = {"archived": {"$in": [False, None]}}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        subscription_uuid = subscription_list[0].get("subscription_uuid")

        for recipient in self.recipients:
            context = self.get_context_data(recipient)
            text_content = render_to_string(f"emails/{path}.txt", context)
            html_content = render_to_string(f"emails/{path}.html", context)
            to = [f"Recipient Name <{recipient}>"]
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.SERVER_EMAIL,
                to=to,
            )
            # add html body to email
            message.attach_alternative(html_content, "text/html")

            # add pdf attachment
            attachment = self.get_attachment(subscription_uuid)
            message.attach(
                "subscription_report.pdf", attachment.read(), "application/pdf"
            )
            message.send(fail_silently=False)
