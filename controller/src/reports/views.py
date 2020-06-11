import logging
import pprint
import statistics
from datetime import timedelta
from itertools import takewhile
# Django Libraries
from django.views.generic import TemplateView

# Local Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.customer_models import CustomerModel, TestModel, validate_customer, validate_test
from api.utils.db_utils import get_single, get_list
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

def get_closest_cycle_within_day_range(subscription,start_date,day_range = 90):
    """
    Get a cycle from a subscription that started the closest to the provided start_date

    Goes through the cycles attached to a subscription and returns the cycles that is closest
    to the start date. Must be within the specified day range as well, if not will return None
    """
    # set initial closest value to the difference between the first cycle and supplied start date
    maximum_date_differnce = timedelta(
        days=day_range
    )
    closest_val = abs(start_date - subscription["cycles"][0]["start_date"])
    # If the initial cycle is within the maximum_data_difference, set it as the cycle before checking others
    if closest_val < maximum_date_differnce:
        active_cycle = subscription["cycles"][0]    
    cycle_start_difference = 0
    for cycle in subscription["cycles"]:
        cycle_start_difference = abs(cycle["start_date"] - start_date)
        print(cycle_start_difference)
        if cycle_start_difference < closest_val and cycle_start_difference < maximum_date_differnce:
            active_cycle = cycle
            closest_val = cycle_start_difference

    if active_cycle:
        return active_cycle
    else:
        print(f"{subscription['subscription_uuid']} does not have a cycle within the specified date range")
        return None

def find_send_timeline_moment(email, timeline_items):
    """
    Look through a statistial summary dictionary and find the tracked record corresponding
    to the provided email
    """
    for moment in timeline_items:
        if moment["email"] == email:
            return moment

def add_moment_no_duplicates(moment,result,message_type):
    """
    Add a timeline moment to the statistical summary, Ignoring duplicates
    """
    
    previous_moment = find_send_timeline_moment(moment["email"],result)
    if message_type in previous_moment:
        return #Do not count duplicates
    previous_moment[message_type] = moment["time"]
    previous_moment[message_type + "_difference"] = moment["time"] - previous_moment["send_time"] 
    return

def append_timeline_moment(moment,result):
    """
    Take a timeline moment and add it to the statisitcal summary for the timeline
    """
    if(moment["message"] == "Email Sent"):
        result.append({
                "email": moment["email"],
                "send_time": moment["time"]
        })
        return
    elif(moment["message"] == "Email Opened"):
        add_moment_no_duplicates(moment,result,"opened_time")
        return
    elif(moment["message"] == "Clicked Link"):
        add_moment_no_duplicates(moment,result,"clicked_time")
        return
    elif(moment["message"] == "Submitted Data"):
        add_moment_no_duplicates(moment,result,"submitted_time")
        return
    elif(moment["message"] == "Email Reported"):
        add_moment_no_duplicates(moment,result,"reported_time")
        return

def generate_time_difference_stats(list_of_times):
    """
    Given a list of time_deltas, determine the min, max, median, avg, and count
    """
    
    count = len(list_of_times)
    avg_val = sum(list_of_times, timedelta()) / count
    min_val =  min(list_of_times)
    median_val =  statistics.median(list_of_times)
    max_val =  max(list_of_times)
    return {
        "count": count,
        "average" : avg_val,
        "minimum" : min_val,
        "median" : median_val,
        "maximum" : max_val,
    }


def generate_campaign_statistics(campaign_timeline_summary):
    """
    Generate campaign statistics based off a campaign_timeline_summary. 

    Returns a list with stats, containing statistics for the campaign. Also returns a full aggregate of the 
    times associated with each possible action (sent,opened,clicked,submitted, and reported) for statistical 
    evaluation at a subscritpion level
    """
    send_times = []
    opened_times = []
    clicked_times = []
    submitted_times = []
    reported_times = []
    for moment in campaign_timeline_summary:
        if "send_time" in moment:
            send_times.append(moment["send_time"])
        if "opened_time" in moment:
            opened_times.append(moment["opened_time_difference"])
        if "clicked_time" in moment:
            clicked_times.append(moment["clicked_time_difference"])
        if "submitted_time" in moment:
            submitted_times.append(moment["submitted_time_difference"])
        if "reported_time" in moment:
            reported_times.append(moment["reported_time_difference"])
    
    stats = {}
    time_aggregate = {}
    if len(send_times):
        stats["send"] = {
            "count": len(send_times)
        }
        time_aggregate["send_times"] = send_times
    if len(opened_times):
        stats["opened"] = generate_time_difference_stats(opened_times)
        time_aggregate["opened_times"] = opened_times
    if len(clicked_times):
        stats["clicked"] = generate_time_difference_stats(clicked_times)
        time_aggregate["clicked_times"] = clicked_times
    if len(submitted_times):
        stats["submitted"] = generate_time_difference_stats(submitted_times)
        time_aggregate["submitted_times"] = submitted_times
    if len(reported_times):
        stats["reported"] = generate_time_difference_stats(reported_times)
        time_aggregate["reported_times"] = reported_times

    return stats, time_aggregate   

def consolidate_campaign_group_stats(campaign_data_list):
    consolidated_times = {
        "send_times" : [],
        "opened_times" : [],
        "clicked_times" : [],
        "submitted_times" : [],
        "reported_times" : [],
    }
    for campaign in campaign_data_list:
        for key in campaign["times"]:
            # consolidated_times[key].append(campaign["times"][key])
            consolidated_times[key] += campaign["times"][key]
            # if key == "send_times":
            #     consolidated_times[key].append(campaign["times"][key])
            # if key == "opened_times":
            #     consolidated_times[key].append(campaign["times"][key])
            # if key == "clicked_times":
            #     consolidated_times[key].append(campaign["times"][key])
            # if key == "submitted_times":
            #     consolidated_times[key].append(campaign["times"][key])
            # if key == "reported_times":
            #     consolidated_times[key].append(campaign["times"][key])
    consolidated_stats = {}
    pp = pprint.PrettyPrinter(indent=4)
    for key in consolidated_times:
        if len(consolidated_times[key]) > 0 and key != "send_times":
            consolidated_stats[key] = generate_time_difference_stats(consolidated_times[key])
        elif len(consolidated_times[key]) > 0 and key == "send_times":
             consolidated_stats[key] = {"count": len(consolidated_times[key])}    
    return consolidated_stats
  
def get_subscription_stats_for_cycle(subscription,start_date = None):
    """
    Generate statistics for a subscriptions given cycle. Determine the cycle by the provided start_date

    """
    results = {}
    results["total_targets"] = len(subscription["target_email_list"])    
    
    active_cycle = get_closest_cycle_within_day_range(subscription, start_date)
    campaigns_in_cycle = []    

    for campaign in subscription["gophish_campaign_list"]:
        if campaign["campaign_id"] in active_cycle["campaigns_in_cycle"]:
            campaigns_in_cycle.append(campaign)

    campaign_timeline_summary = []
    campaign_results = []
    subscirption_results = []

    for campaign in campaigns_in_cycle:
        for moment in campaign["timeline"]:
            append_timeline_moment(moment,campaign_timeline_summary)
        stats, time_aggregate = generate_campaign_statistics(campaign_timeline_summary)
        campaign_results.append({
            "campaign_id": campaign["campaign_id"],
            "deception_level": campaign["deception_level"],
            # "time_line_summary": campaign_timeline_summary
            "campaign_stats": stats, 
            "times": time_aggregate
        })        
        campaign_timeline_summary = []

    low_deception_campaigns = list(filter(lambda x: x["deception_level"] == 1, campaign_results))
    medium_deception_campaigns = list(filter(lambda x: x["deception_level"] == 2, campaign_results))
    high_deception_campaigns = list(filter(lambda x: x["deception_level"] == 3, campaign_results))


    consolidated_stats = consolidate_campaign_group_stats(campaign_results)
    low_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 1, campaign_results)))
    medium_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 2, campaign_results)))
    high_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 3, campaign_results)))

    pp = pprint.PrettyPrinter(indent=4)
    print("Low =====================")
    pp.pprint(low_decp_stats)
    print("Medium =====================")
    pp.pprint(medium_decp_stats)
    print("High =====================")
    pp.pprint(high_decp_stats)
    print("Combined =====================")
    pp.pprint(consolidated_stats)
    # for i in campaign_results:
    #     pp.pprint(i)

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
            "full_name" : _customer.get("name"),
            "short_name" : _customer.get("identifier"),
            "poc_name" : None,
            "poc_email" : None,
            "vulnerabilty_team_lead_name" : None,
            "vulnerabilty_team_lead_email" : None,
        }
        cycles = subscription["cycles"]
        for cycle in subscription["cycles"]:
            if cycle["start_date"] == start_date:
                current_cycle = cycle
        if cycle is None:
            return "Cycle not found"
        dates = {
            "start" : cycle["start_date"],
            "end" : cycle["end_date"],
        }
        
        total_users_targeted = len(subscription["target_email_list"])

        campaigns_in_cycle = []



        metrics = {
            "total_users_targeted" :  total_users_targeted,
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

        line_sep = "===================================================================================="
        print(line_sep)
        # parameters = {}
        # parameters = {"sector": "Chemical","city": ["Santa Cruz" }
        parameters = {"sector": _customer['sector']}
        fields = { 
            "customer_uuid": 1, 
            "sector": 1,
            "industry": 1,
            }
        # parameters = {{"sector": "Chemical" },{"sector: 1"}}
        customer_list = get_list(
            parameters, "customer", TestModel, validate_test, fields
        )
        sector_customer_uuids = []
        industry_customer_uuids = []
        for cust in customer_list:
            sector_customer_uuids.append(cust["customer_uuid"])
            if cust["industry"] == _customer["industry"]:
                industry_customer_uuids.append(cust["customer_uuid"])
        
        parameters = {
            "active": True
        }
        sub_fields = { 
            "customer_uuid": 1, 
            "subscription_uuid": 1,
            "gophish_campaign_list": 1,
            "cycles": 1,
        }
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription, sub_fields
        )
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(subscription_list[0])
        # pp.pprint(customer_list)
        # get_subscription_stats_for_cycle(subscription,subscription["cycles"][0]["start_date"])


        return context
