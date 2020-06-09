import logging

# Django Libraries
from django.views.generic import TemplateView

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.customer_models import CustomerModel, validate_customer
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

class QuarterlyReports(TemplateView):
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


    template_name = "reports/quarterly.html"    

    def get_context_data(self, **kwargs):

        # Get Args from url
        subscription_uuid = self.kwargs["subscription_uuid"]
        start_date = self.kwargs["start_date"]

        # Get targeted subscription and associated customer data
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
        _customer = get_single(
            subscription.get("customer_uuid"),"customer",CustomerModel,validate_customer            
        )
        
        #Build out return data
        company = {
            "name" : _customer.get("name"),
            "address" : f"{_customer.get('address_1')} {_customer.get('address_2')}",
        }
        subscription_primary_contact = subscription.get("primary_contact")
        DHS_contact = {
            "group" : None,
            "email" : None,
        }
        # TODO : figure out who to use as customer POC, or if all need to be listed
        # TODO : figure out who to use as vulnerability_team_lead
        customer = {
            "full_name" : customer.get("name"),
            "short_name" : customer.get("identifier"),
            "poc_name" : None,
            "poc_email" : None,
            "vulnerabilty_team_lead_name" : None,
            "vulnerabilty_team_lead_email" : None,
        }
        for cycle in subscription["cycles"]:
            if cycle["start_date"] == start_date:
                current_cycle = cycle
        if cycle is None:
            return "Cycle not found"
        dates = {
            "start" : cycle["start_date"],
            "end" : cycle["end_date"],
        }
        quarters = subscription["cycles"]
        
        metrics = {
            "total_users_targeted" : 0 ,
            "number_of_email_sent_overall" : 0 ,
            "number_of_clicked emails" : 0 ,
            "number_of_phished_users_overall" : 0 ,
            "number_of_reports_to_helpdesk" : 0 ,
            "repots_to_clicks_ratio" : 0 ,
            "avg_time_to_first_click" : 0 ,
            "avg_time_to_first_report" : 0 ,
            "most_successful_template" : 0 ,
        }

        context = {}
        context["subscription_uuid"] = subscription_uuid
        context["company"] = company
        context["subscription_primary_contact"] = subscription_primary_contact
        context["DHS_contact"] = DHS_contact
        context["customer"] = customer
        context["dates"] = dates
        context["cycles"] = cycles
        context["metrics"] = metrics

        return context
