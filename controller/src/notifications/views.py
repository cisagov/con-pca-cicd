# Standard Libraries
from typing import List, Any
from email.mime.image import MIMEImage

# Django Libraries
from django.conf import settings
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

# Third-Party Libraries
from weasyprint import HTML

# Local Libraries
from notifications.utils import get_notification
from api.utils.db_utils import get_list
from api.models.subscription_models import SubscriptionModel, validate_subscription


class ReportsEmailSender:
    def __init__(self, message_type: str):
        self.message_type = message_type

    def get_context_data(self, first_name, last_name):
        context: Dict[str, Any] = {}
        context["first_name"] = first_name
        context["last_name"] = last_name
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
        subscription = subscription_list[0]

        # pull subscription data
        subscription_uuid = subscription.get("subscription_uuid")
        recipient = subscription.get("primary_contact").get("email")
        recipient_copy = subscription.get("dhs_primary_contact").get("email")
        first_name = subscription.get("primary_contact").get("first_name")
        last_name = subscription.get("primary_contact").get("last_name")

        # pass context to email templates
        context = self.get_context_data(first_name, last_name)
        text_content = render_to_string(f"emails/{path}.txt", context)
        html_content = render_to_string(f"emails/{path}.html", context)

        to = [f"{first_name} {last_name} <{recipient}>"]
        bcc = [f"DHS <{recipient_copy}>"]
        message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.SERVER_EMAIL,
            to=to,
            bcc=bcc,
        )

        # pass image files
        image_files = ["cisa_logo.png"]
        for image_file in image_files:
            with staticfiles_storage.open(f"img/{image_file}") as f:
                header = MIMEImage(f.read())
                header.add_header("Content-ID", f"<{image_file}>")
                message.attach(header)

        # add html body to email
        message.attach_alternative(html_content, "text/html")

        # add pdf attachment
        attachment = self.get_attachment(subscription_uuid)
        message.attach("subscription_report.pdf", attachment.read(), "application/pdf")
        message.send(fail_silently=False)
