# Standard Python Libraries
from datetime import datetime
import logging
import base64

# Third-Party Libraries
# Local Libraries
# Django Libraries
from scipy.stats.mstats import gmean
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
    get_closest_cycle_within_day_range,
    ratio_to_percent,
    format_timedelta,
    get_statistic_from_region_group
)

logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()


class MonthlyReportsView(TemplateView):
    """
    Monthly reports
    """

    template_name = "reports/monthly.html"

    def calculateSvgCircles(self, numerator, denominator):
        # given the numerator and total calculate and
        # return the svg circle
        ratio = round(
            float(numerator or 0) / float(1 if denominator is None else denominator), 2
        )
        percentage = ratio * 100
        remaining_percentage = 100 - percentage
        svgstring = """<svg width="100%" height="100%" viewBox="0 0 42 42" class="donut" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <circle class="donut-hole" cx="21" cy="21" r="14" fill="#fff"></circle>
                    <circle class="donut-ring" cx="21" cy="21" r="14" fill="transparent" stroke="#cecece" stroke-width="6"></circle><circle class="donut-segment" cx="21" cy="21" r="14" fill="transparent" stroke="#164A91" stroke-width="6" stroke-dasharray="{} {}" stroke-dashoffset="25"></circle>
                    </svg>""".format(
            percentage, remaining_percentage
        )
        return svgstring

    def getMonthlyStats(self, subscription):
        start_date = subscription["start_date"]
        # Get statistics for the specified subscription during the specified cycle
        subscription_stats = get_subscription_stats_for_cycle(subscription, start_date)
        opened = get_statistic_from_group(
            subscription_stats, "stats_all", "opened", "count"
        )
        clicked = get_statistic_from_group(
            subscription_stats, "stats_all", "clicked", "count"
        )
        sent = get_statistic_from_group(
            subscription_stats, "stats_all", "sent", "count"
        )
        submitted = get_statistic_from_group(
            subscription_stats, "stats_all", "submitted", "count"
        )
        reported = get_statistic_from_group(
            subscription_stats, "stats_all", "reported", "count"
        )

        total = len(subscription["target_email_list"])
        metrics = {
            "total_users_targeted": total,
            "number_of_email_sent_overall": sent,
            "number_of_clicked_emails": clicked,
            "percent_of_clicked_emails": round(
                float(clicked or 0) / float(1 if sent is None else sent), 2
            ),
            "number_of_opened_emails": opened,
            "number_of_phished_users_overall": total,
            "percent_of_phished_users_overall": round(
                float(clicked or 0) / float(1 if total is None else total), 2
            ),
            "number_of_reports_to_helpdesk": reported,
            "percent_report_rate": round(
                float(reported or 0) / float(1 if opened is None else opened), 2
            ),
            "reports_to_clicks_ratio": get_reports_to_click(subscription_stats),
            "avg_time_to_first_click": get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "average"
            ),
            "avg_time_to_first_report": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "average"
            ),
            "ratio_reports_to_clicks": round(
                float(reported or 0) / float(1 if clicked is None else clicked), 2
            ),
        }
        return metrics

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

        metrics = self.getMonthlyStats(subscription)

        customer_address = """{},\n{}""".format(
            customer.get("address_1"), customer.get("address_2")
        )

        customer_address_2 = """{}, {} {} USA""".format(
            customer.get("city"), customer.get("state"), customer.get("zip_code"),
        )

        dhs_contact_name = "{} {}".format(
            dhs_contact.get("first_name"), dhs_contact.get("last_name")
        )

        primary_contact = subscription.get("primary_contact")
        primary_contact_name = "{} {}".format(
            primary_contact.get("first_name"), primary_contact.get("last_name")
        )

        total_users_targeted = len(subscription["target_email_list"])
        svg_circle_sent = self.calculateSvgCircles(
            metrics["number_of_email_sent_overall"], total_users_targeted
        )
        svg_circle_opened = self.calculateSvgCircles(
            metrics["number_of_opened_emails"], total_users_targeted
        )
        svg_circle_clicked = self.calculateSvgCircles(
            metrics["number_of_clicked_emails"], total_users_targeted
        )

        context = {
            # Customer info
            "customer_name": customer.get("name"),
            "customer_identifier": customer.get("identifier"),
            "customer_address": customer_address,
            "customer_address_2": customer_address_2,
            # primary contact info
            "primary_contact_name": primary_contact_name,
            "primary_contact_email": primary_contact.get("email"),
            # DHS contact info
            "dhs_contact_name": dhs_contact_name,
            "dhs_contact_email": dhs_contact.get("email"),
            "dhs_contact_mobile_phone": dhs_contact.get("office_phone"),
            "dhs_contact_office_phone": dhs_contact.get("mobile_phone"),
            # Subscription info
            "start_date": subscription.get("start_date"),
            "end_date": subscription.get("end_date"),
            "target_count": target_count,
            "metrics": metrics,
            "sent_circle_svg": base64.b64encode(svg_circle_sent.encode("ascii")).decode(
                "ascii"
            ),
            "opened_circle_svg": base64.b64encode(
                svg_circle_opened.encode("ascii")
            ).decode("ascii"),
            "clicked_circle_svg": base64.b64encode(
                svg_circle_clicked.encode("ascii")
            ).decode("ascii"),
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

        subscription_primary_contact = subscription.get("primary_contact")

        customer = {
            "full_name": _customer.get("name"),
            "short_name": _customer.get("identifier"),
            "address_1": _customer.get("address_1"),
            "address_2": _customer.get("address_2"),
            "identifier": _customer.get("identifier"),
            "poc_email": None,
            "vulnerabilty_team_lead_name": None,
            "vulnerabilty_team_lead_email": None,
        }
        cycles = subscription["cycles"]
        cycles = sorted(cycles,key=lambda cycle: cycle["start_date"]) 
        working_cycle_year = cycles[0]["start_date"].year
        current_quarter = 1  
        # Count the cycle order from the year or try to match up to standard 'quarters'?
        for cycle in cycles:
            if cycle["start_date"].year > working_cycle_year:
                current_quarter = 1
            cycle["quarter"] = f"{cycle['start_date'].year} - {current_quarter}"


        # for i, cycle in enumerate(cycles,1):
        #     if
        #     cycle["quarter"] = quarter

        current_cycle = ""
        for cycle in subscription["cycles"]:
            if cycle["start_date"] == start_date:
                current_cycle = cycle
            else:
                current_cycle = get_closest_cycle_within_day_range(
                    subscription, start_date
                )
        # if cycle is None:
        #     return "Cycle not found"
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
            "percent_of_clicked_emails": ratio_to_percent(get_statistic_from_group(
                subscription_stats, "stats_all", "ratios", "clicked_ratio"
            )),
            "percent_of_submits": ratio_to_percent(get_statistic_from_group(
                subscription_stats, "stats_all", "ratios", "submitted_ratio"
            )),
            "number_of_opened_emails": get_statistic_from_group(
                subscription_stats, "stats_all", "opened", "count"
            ),
            "number_of_phished_users_overall": get_statistic_from_group(
                subscription_stats, "stats_all", "submitted", "count"
            ),
            "percent_report_rate": ratio_to_percent(get_statistic_from_group(
                subscription_stats, "stats_all", "ratios", "reported_ratio"
            )),
            "number_of_reports_to_helpdesk": get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "count"
            ),
            "repots_to_clicks_ratio": round(get_reports_to_click(subscription_stats),2),
            "avg_time_to_first_click": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "clicked", "average"
            )),
            "avg_time_to_first_report": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "average"
            )),
            "most_successful_template": campaign_templates_to_string(
                get_most_successful_campaigns(subscription_stats, "reported")
            ),
            "emails_sent_over_target_count": round(get_statistic_from_group(
                subscription_stats, "stats_all", "sent", "count"
            ) / len(subscription["target_email_list"]),0),
            "customer_clicked_avg": ratio_to_percent(get_statistic_from_region_group(
                region_stats,"customer","clicked_ratio"
            ),0),
            "national_clicked_avg": ratio_to_percent(get_statistic_from_region_group(
                region_stats,"national","clicked_ratio"
            ),0),
            "industry_clicked_avg": ratio_to_percent(get_statistic_from_region_group(
                region_stats,"industry","clicked_ratio"
            ),0),
            "sector_clicked_avg": ratio_to_percent(get_statistic_from_region_group(
                region_stats,"sector","clicked_ratio"
            ),0),
            "shortest_time_to_open": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "opened", "minimum"
            )),
            "shortest_time_to_report": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "minimum"
            )),
            "median_time_to_report": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "reported", "median"
            )),
            "longest_time_to_open": format_timedelta(get_statistic_from_group(
                subscription_stats, "stats_all", "opened", "maximum"
            )),
        }

        # ------
        dhs_contact = get_single(
            subscription.get("dhs_contact_uuid"),
            "dhs_contact",
            DHSContactModel,
            validate_dhs_contact,
        )
        dhs_contact_name = (
            f"{dhs_contact.get('first_name')} {dhs_contact.get('last_name')}"
        )
        primary_contact = subscription.get("primary_contact")



        context = {}
        context["dhs_contact_name"] = dhs_contact_name
        context["subscription_uuid"] = subscription_uuid
        context["primary_contact"] = primary_contact
        context["primary_contact_email"] = primary_contact.get("email")
        context["company"] = company
        context["subscription_primary_contact"] = subscription_primary_contact
        context["DHS_contact"] = dhs_contact
        context["customer"] = customer
        context["dates"] = dates
        context["cycles"] = cycles
        context["target_cycle"] = current_cycle
        context["metrics"] = metrics
        context["previous_cycles"] = previous_cycle_stats
        context["region_stats"] = region_stats
        context["subscription_stats"] = subscription_stats

        return context
