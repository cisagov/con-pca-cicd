# Standard Python Libraries
from datetime import datetime
import logging

# Third-Party Libraries
# Local Libraries
# Django Libraries
from api.manager import CampaignManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.customer_models import CustomerModel, validate_customer
from api.models.dhs_models import DHSContactModel, validate_dhs_contact
from api.utils.db_utils import get_list, get_single
from django.views.generic import TemplateView

from . import views
from .utils import (
    get_subscription_stats_for_cycle,
    get_related_subscription_stats,
    get_cycles_breakdown,
    get_template_details,
    get_statistic_from_group,
    get_reports_to_click,
    campaign_templates_to_string,
    get_most_successful_campaigns,
)

logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()


class MonthlyReportsView(TemplateView):
    """
    Monthly reports
    """

    template_name = "reports/monthly.html"

    def get_context_data(self, **kwargs):
        subscription_uuid = self.kwargs["subscription_uuid"]
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        customer = get_single(
            subscription.get("customer_uuid"),
            "customer",
            CustomerModel,
            validate_customer,
        )

        dhs_contact = get_single(
            subscription.get("dhs_contact_uuid"),
            "dhs_contact",
            DHSContactModel,
            validate_dhs_contact,
        )
        campaigns = subscription.get("gophish_campaign_list")
        summary = [
            campaign_manager.get("summary", campaign_id=campaign.get("campaign_id"))
            for campaign in campaigns
        ]
        target_count = sum([targets.get("stats").get("total") for targets in summary])

        customer_address = """
        {} {},
        {} USA {}
        """.format(
            customer.get("address_1"),
            customer.get("address_2"),
            customer.get("state"),
            customer.get("zip_code"),
        )

        dhs_contact_name = "{} {}".format(
            dhs_contact.get("first_name"), dhs_contact.get("last_name")
        )

        context = {
            # Customer info
            "customer_name": customer.get("name"),
            "customer_identifier": customer.get("identifier"),
            "customer_address": customer_address,
            # DHS contact info
            "dhs_contact_name": dhs_contact_name,
            "dhs_contact_email": dhs_contact.get("email"),
            "dhs_contact_mobile_phone": dhs_contact.get("office_phone"),
            "dhs_contact_office_phone": dhs_contact.get("mobile_phone"),
            # Subscription info
            "start_date": subscription.get("start_date"),
            "end_date": subscription.get("end_date"),
            "target_count": target_count,
        }

        return context


class CycleReportsView(TemplateView):
    """
    Cycle Reports
    """

    template_name = "reports/cycle.html"

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


class YearlyReportsView(TemplateView):
    """
    Yearly Reports
    """

    template_name = "reports/yearly.html"

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
            "dhs_contact_name": dhs_contact.get("name"),
            "start_date": summary[0].get("created_date"),
            "end_date": summary[0].get("send_by_date"),
            "target_count": target_count,
        }

        return context


class CycleReports(TemplateView):
    # DATA NEEDED
    # Compnay
    #     - name
    #     - address
    # SubscriptionPrimaryContact
    #     - name
    #     - phone
    #     - email
    # DHS Contact
    #     - Organization/teamname/group
    #     - email
    # Customer
    #     - full_name
    #     - short_name
    #     - poc_name
    #     - poc_email
    #     - Vulnerability Managment Team Lead
    # Dates
    #     - start_date
    #     - end_date
    # Quarters[] (previous)
    #     - quarter
    #         - quarter (2020-Q1)
    #         - start_date (January 1, 2020 - March 30, 2020)
    #         - end_date (April 1, 2020 - June 30, 2020)
    #         - note (UNKNOWN)
    # Metrics
    #     - total_users_targeted
    #     - number_of_email_sent_overall
    #     - number_of_clicked emails
    #     - number_of_phished_users_overall
    #     - number_of_reports_to_helpdesk
    #     - repots_to_clicks_ratio
    #     - avg_time_to_first_click
    #     - avg_time_to_first_report
    #     - most_successful_template
    template_name = "reports/cycle.html"

    def get_context_data(self, **kwargs):
        """
        Generate the cycle report based off of the provided start date
        """
        # Get Args from url
        subscription_uuid = self.kwargs["subscription_uuid"]

        # Get targeted subscription and associated customer data
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )

        _customer = get_single(
            subscription.get("customer_uuid"),
            "customer",
            CustomerModel,
            validate_customer,
        )

        company = {
            "name": _customer.get("name"),
            "address": f"{_customer.get('address_1')} {_customer.get('address_2')}",
        }

        start_date = subscription["start_date"]

        # TODO : Fill in DHS contact when it has been added
        subscription_primary_contact = subscription.get("primary_contact")
        DHS_contact = {
            "group": None,
            "email": None,
        }
        # TODO : figure out who to use as customer POC, or if all need to be listed
        # TODO : figure out who to use as vulnerability_team_lead
        customer = {
            "full_name": _customer.get("name"),
            "short_name": _customer.get("identifier"),
            "poc_name": None,
            "poc_email": None,
            "vulnerabilty_team_lead_name": None,
            "vulnerabilty_team_lead_email": None,
        }
        cycles = subscription["cycles"]
        current_cycle = ""
        for cycle in subscription["cycles"]:
            if cycle["start_date"] == start_date:
                current_cycle = cycle
        if cycle is None:
            return "Cycle not found"
        dates = {
            "start": cycle["start_date"],
            "end": cycle["end_date"],
        }

        # Get statistics for the specified subscription during the specified cycle
        subscription_stats = get_subscription_stats_for_cycle(subscription, start_date)
        region_stats = get_related_subscription_stats(subscription, start_date)
        previous_cycle_stats = get_cycles_breakdown(subscription["cycles"])

        # Get template details for each campaign template
        get_template_details(subscription_stats["campaign_results"])

        metrics = {
            "total_users_targeted": len(subscription["target_email_list"]),
            "number_of_email_sent_overall": get_statistic_from_group(
                subscription_stats, "stats_all", "sent", "count"
            ),
            "number_of_clicked_emails": get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "count"
            ),
            "number_of_opened_emails": get_statistic_from_group(
                subscription_stats, "stats_all", "opened", "count"
            ),
            "number_of_phished_users_overall": get_statistic_from_group(
                subscription_stats, "stats_all", "submitted", "count"
            ),
            "number_of_reports_to_helpdesk": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "count"
            ),
            "repots_to_clicks_ratio": get_reports_to_click(subscription_stats),
            "avg_time_to_first_click": get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "average"
            ),
            "avg_time_to_first_report": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "average"
            ),
            "most_successful_template": campaign_templates_to_string(
                get_most_successful_campaigns(subscription_stats, "reported")
            ),
        }

        context = {}
        context["subscription_uuid"] = subscription_uuid
        context["company"] = company
        context["subscription_primary_contact"] = subscription_primary_contact
        context["DHS_contact"] = DHS_contact
        context["customer"] = customer
        context["dates"] = dates
        context["cycles"] = cycles
        context["target_cycle"] = current_cycle
        context["metrics"] = metrics
        context["previous_cycles"] = previous_cycle_stats
        context["region_stats"] = region_stats
        context["subscription_stats"] = subscription_stats

        return context
