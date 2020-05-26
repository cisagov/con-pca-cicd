import logging

from weasyprint import HTML

from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import path
from django.conf.urls import url
from django.template.loader import get_template
from django.http import HttpResponse, FileResponse

from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.utils.db_utils import get_single
from api.manager import CampaignManager
from . import views


logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()


class ReportsView(TemplateView):
    template_name = "reports/base.html"

    def get_context_data(self, **kwargs):
        subscription_uuid = self.kwargs["subscription_uuid"]
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        campaigns = subscription.get("gophish_campaign_list")
        summary = [
            campaign_manager.get("summary", campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]
        target_count = sum([targets.get("stats").get("total") for targets in summary])
        context = {
            "subscription_uuid": subscription_uuid,
            "customer_name": subscription.get("name"),
            "start_date": summary[0].get("created_date"),
            "end_date": summary[0].get("send_by_date"),
            "target_count": target_count,
        }
        return context


def generate_pdf(request):
    html = HTML("http://localhost:8000/reports/")
    html.write_pdf("/tmp/reports_test.pdf")

    fs = FileSystemStorage("/tmp")
    with fs.open("reports_test.pdf") as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="subscription_report.pdf"'
        return response
    return response
