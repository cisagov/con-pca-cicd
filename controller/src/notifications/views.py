"""
Notifications views.

This is the core of gerating emails to send to
contacts about reports and subscription updates.
"""


# Standard Python Libraries
<<<<<<< HEAD
=======
# Standard Libraries
>>>>>>> adding exists to db uitls
from datetime import datetime
from email.mime.image import MIMEImage

# Django Libraries
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

# Local Libraries
from api.models.dhs_models import DHSContactModel, validate_dhs_contact
from notifications.utils import get_notification
from weasyprint import HTML
from api.utils.db_utils import get_single


class ReportsEmailSender:
    """ReportsEmailSender class."""

    def __init__(self, subscription, message_type):
        """Init method."""
        self.subscription = subscription
        self.message_type = message_type

    def get_attachment(self, subscription_uuid):
        """Get_attachment method."""
        html = HTML(f"http://localhost:8000/reports/{subscription_uuid}/")
        html.write_pdf("/storage/subscription_report.pdf")  # change to AWS storage var
        fs = FileSystemStorage("/storage")
        return fs.open("subscription_report.pdf")

    def send(self):
        """Send method."""
        subject, path = get_notification(self.message_type)

        # pull subscription data
        subscription_uuid = self.subscription.get("subscription_uuid")
        recipient = self.subscription.get("primary_contact").get("email")
        dhs_contact_uuid = self.subscription.get("dhs_contact_uuid")
        recipient_copy = get_single(
            dhs_contact_uuid, "dhs_contact", DHSContactModel, validate_dhs_contact
        )
        recipient_copy = recipient_copy.get("email")
        first_name = self.subscription.get("primary_contact").get("first_name")
        last_name = self.subscription.get("primary_contact").get("last_name")

        # pass context to email templates
        context = {"first_name": first_name, "last_name": last_name}

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


class SubscriptionNotificationEmailSender:
    """NotificationEmailSender class."""

    def __init__(self, subscription, notification_type):
        """Init method."""
        self.subscription = subscription
        self.notification_type = notification_type

    def create_context_data(self):
        """Create Contect Data Method."""
        first_name = self.subscription.get("primary_contact").get("first_name")
        last_name = self.subscription.get("primary_contact").get("last_name")

        try:
            start_date = datetime.strptime(
                self.subscription.get("start_date"), "%Y-%m-%dT%H:%M:%S"
            ).strftime("%d %B, %Y")
            end_date = self.subscription.get("end_date")
            if end_date is not None:
                end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S").strftime(
                    "%d %B, %Y"
                )
        except AttributeError:
            # datetime is a string and needs to be converted and reformated
            string_start_date = self.subscription.get("start_date")
            string_end_date = self.subscription.get("end_date")
            dt_start_date = datetime.strptime(string_start_date, "%Y-%m-%dT%H:%M:%S")
            dt_end_date = datetime.strptime(string_end_date, "%Y-%m-%dT%H:%M:%S")
            start_date = dt_start_date.strftime("%d %B, %Y")
            end_date = dt_end_date.strftime("%d %B, %Y")

        start_date = self.subscription.get("start_date").strftime("%d %B, %Y")
        end_date = self.subscription.get("end_date").strftime("%d %B, %Y")
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "start_date": start_date,
            "end_date": end_date,
        }

    def send(self):
        """Send method."""
        subject, path = get_notification(self.notification_type)

        # pull subscription data
        recipient = self.subscription.get("primary_contact").get("email")

        # get to and bcc email addresses
        dhs_contact_uuid = self.subscription.get("dhs_contact_uuid")
        recipient_copy = get_single(
            dhs_contact_uuid, "dhs_contact", DHSContactModel, validate_dhs_contact
        )
        recipient_copy = recipient_copy.get("email")

        # pass context to email templates
        context = self.create_context_data()
        text_content = render_to_string(f"emails/{path}.txt", context)
        html_content = render_to_string(f"emails/{path}.html", context)

        to = [f"{context['first_name']} {context['last_name']} <{recipient}>"]
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
        message.send(fail_silently=False)
