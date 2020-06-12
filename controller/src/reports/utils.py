from datetime import timedelta
from itertools import takewhile
import statistics

from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
from api.models.customer_models import CustomerModel, TestModel, validate_customer, validate_test
from api.utils.db_utils import get_single, get_list

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
        closest_cycle = subscription["cycles"][0]    
    cycle_start_difference = 0
    for cycle in subscription["cycles"]:
        cycle_start_difference = abs(cycle["start_date"] - start_date)
        if cycle_start_difference < closest_val and cycle_start_difference < maximum_date_differnce:
            closest_cycle = cycle
            closest_val = cycle_start_difference

    if closest_cycle:
        return closest_cycle
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
    previous_moment[message_type + "_difference"] = moment["time"] - previous_moment["sent"] 
    return

def append_timeline_moment(moment,result):
    """
    Take a timeline moment and add it to the statisitcal summary for the timeline
    """

    if(moment["message"] == "Email Sent"):
        result.append({
                "email": moment["email"],
                "sent": moment["time"]
        })
        return
    elif(moment["message"] == "Email Opened"):
        add_moment_no_duplicates(moment,result,"opened")
        return
    elif(moment["message"] == "Clicked Link"):
        add_moment_no_duplicates(moment,result,"clicked")
        return
    elif(moment["message"] == "Submitted Data"):
        add_moment_no_duplicates(moment,result,"submitted")
        return
    elif(moment["message"] == "Email Reported"):
        add_moment_no_duplicates(moment,result,"reported")
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
        if "sent" in moment:
            send_times.append(moment["sent"])
        if "opened" in moment:
            opened_times.append(moment["opened_difference"])
        if "clicked" in moment:
            clicked_times.append(moment["clicked_difference"])
        if "submitted" in moment:
            submitted_times.append(moment["submitted_difference"])
        if "reported" in moment:
            reported_times.append(moment["reported_difference"])
    
    stats = {}
    time_aggregate = {}
    if len(send_times):
        stats["sent"] = {
            "count": len(send_times)
        }
        time_aggregate["sent"] = send_times
    if len(opened_times):
        stats["opened"] = generate_time_difference_stats(opened_times)
        time_aggregate["opened"] = opened_times
    if len(clicked_times):
        stats["clicked"] = generate_time_difference_stats(clicked_times)
        time_aggregate["clicked"] = clicked_times
    if len(submitted_times):
        stats["submitted"] = generate_time_difference_stats(submitted_times)
        time_aggregate["submitted"] = submitted_times
    if len(reported_times):
        stats["reported"] = generate_time_difference_stats(reported_times)
        time_aggregate["reported"] = reported_times

    return stats, time_aggregate   

def consolidate_campaign_group_stats(campaign_data_list):
    consolidated_times = {
        "sent" : [],
        "opened" : [],
        "clicked" : [],
        "submitted" : [],
        "reported" : [],
    }
    for campaign in campaign_data_list:
        for key in campaign["times"]:
            consolidated_times[key] += campaign["times"][key]
    consolidated_stats = {}
    for key in consolidated_times:
        if len(consolidated_times[key]) > 0 and key != "sent":
            consolidated_stats[key] = generate_time_difference_stats(consolidated_times[key])
        elif len(consolidated_times[key]) > 0 and key == "sent":
            consolidated_stats[key] = {"count": len(consolidated_times[key])}    
    return consolidated_stats

def calc_ratios(campaign_stats):
    """
    Calc the ratios for a given list of phishing results

    Accepts click breakdown model or phish_results model and converts
    the provided stats to the necesary format for computation.
    """
    #Convert to proper format for computation if not already
    working_vals = {}
    if campaign_stats:
        key_check = next(iter(campaign_stats))
        if key_check:            
            if isinstance(campaign_stats[key_check], dict):
                for key in campaign_stats:
                    working_vals[key] = campaign_stats[key]["count"]
            else:
                working_vals = campaign_stats
    clicked_ratio, opened_ratio, submitted_ratio, reported_ratio = None, None, None, None
    
    #Get ratios
    if "sent" in working_vals:        
        #Make sure you dont divide by zero        
        if working_vals["sent"] != 0:
            if "clicked" in working_vals:
                clicked_ratio = working_vals["clicked"] / working_vals["sent"]
            if "opened" in working_vals:
                opened_ratio = working_vals["opened"] / working_vals["sent"]
            if "submitted" in working_vals:
                submitted_ratio = working_vals["submitted"] / working_vals["sent"]
            if "reported" in working_vals:
                reported_ratio = working_vals["reported"] / working_vals["sent"]
    return { 
        "clicked_ratio" : clicked_ratio, 
        "opened_ratio" : opened_ratio, 
        "submitted_ratio" : submitted_ratio, 
        "reported_ratio" : reported_ratio 
        }

def get_clicked_time_period_breakdown(campaign_results):
    """
    Get the clicked breakdown over time in ratio form. 

    Takes campaign results list and generates a ratio for how many clicks have occured
    during each specified time delta (time deltas pulled from current cycle report example)
    """

    time_deltas = {
        "one_minute": (timedelta(minutes=1),1),
        "three_minutes": (timedelta(minutes=3),2),
        "five_minutes": (timedelta(minutes=5),3),
        "fifteen_minutes": (timedelta(minutes=15),4),
        "thirty_minutes": (timedelta(minutes=30),5),
        "one_hour": (timedelta(hours=1),6),
        "two_hours": (timedelta(hours=2),7),
        "three_hours": (timedelta(hours=3),8),
        "four_hours": (timedelta(hours=4),9),
        "one_day": (timedelta(days=1),10),
    }
    time_counts = {}
    clicked_ratios = {}
    for key in time_deltas:
        time_counts[key] = 0
        clicked_ratios[key] = None
    
    clicked_count = 0
    for campaign in campaign_results:
        if "clicked" in campaign["times"]:
            for moment in campaign["times"]["clicked"]:
                for key in time_deltas:
                    if moment < time_deltas[key][0]:
                        clicked_count += 1
                        time_counts[key] += 1
                        break
    
    last_key = None
    if clicked_count:
        for i, key in enumerate(time_counts, 0):
            if not last_key:
                last_key = key
            else:
                time_counts[key] += time_counts[last_key]
                clicked_ratios[key] = time_counts[key] / clicked_count
                last_key = key

    return clicked_ratios

def get_subscription_stats_for_cycle(subscription,start_date = None):
    """
    Generate statistics for a subscriptions given cycle. Determine the cycle by the provided start_date

    """

    results = {}
    total_targets = len(subscription["target_email_list"])    

    # Get the correct cycle based on the provided start_date
    active_cycle = get_closest_cycle_within_day_range(subscription, start_date)
      
    # Get all the campaigns for the specified cycle from the gophish_campaign_list
    campaigns_in_cycle = []  
    for campaign in subscription["gophish_campaign_list"]:
        if campaign["campaign_id"] in active_cycle["campaigns_in_cycle"]:
            campaigns_in_cycle.append(campaign)

    # Loop through all campaigns in cycle. Check for unique moments, and appending to campaign_timeline_summary
    campaign_timeline_summary = []
    campaign_results = []
    subscirption_results = []
    for campaign in campaigns_in_cycle:
        for moment in campaign["timeline"]:
            if not moment["duplicate"]:
                append_timeline_moment(moment,campaign_timeline_summary)
        # Get stats and aggregate of all time differences (all times needed for stats like median when consolidated)
        stats, time_aggregate = generate_campaign_statistics(campaign_timeline_summary)
        campaign_results.append({
            "campaign_id": campaign["campaign_id"],
            "deception_level": campaign["deception_level"],
            "campaign_stats": stats, 
            "times": time_aggregate,
            "ratios": calc_ratios(stats),
            "template_name": campaign["email_template"],
            "template_uuid" : campaign["template_uuid"],
        })        
        campaign_timeline_summary = []

    #generate campaign_group stats based off deception level and oconsolidation of all campaigns
    consolidated_stats = consolidate_campaign_group_stats(campaign_results)
    low_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 1, campaign_results)))
    medium_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 2, campaign_results)))
    high_decp_stats = consolidate_campaign_group_stats(list(filter(lambda x: x["deception_level"] == 3, campaign_results)))
    clicks_over_time = get_clicked_time_period_breakdown(campaign_results)



    return {
        "campaign_results": campaign_results,
        "stats_all": consolidated_stats,
        "stats_low_deception": low_decp_stats,
        "stats_mid_deception": medium_decp_stats,
        "stats_high_deception": high_decp_stats,
        "clicks_over_time": clicks_over_time,
    }

def generate_region_stats(subscription_list, cycle_date = None):
    """
    Generate statistics for multiple subscriptions. Can provide cycle_date to specify a cycle range to use

    Given a list of subscriptions, get the phishing results from the cycle value and summarize.
    """

    region_stats = {}
    campaign_count = 0
    for subscription in subscription_list:
        target_cycles = []
        if cycle_date:
            target_cycles.append(get_closest_cycle_within_day_range(subscription,cycle_date))
        else:
            target_cycles = subscription["cycles"]
        for target_cycle in target_cycles:
            campaign_count += len(target_cycle["campaigns_in_cycle"])
            if not region_stats:
                region_stats = target_cycle["phish_results"].copy()
            else:
                for key in target_cycle["phish_results"]:
                    region_stats[key] += target_cycle["phish_results"][key]    
    
    ratios = calc_ratios(region_stats)
    ret_val = {
        "consolidated_values": region_stats,
        "subscription_count": len(subscription_list),
        "campaign_count": campaign_count,
        "clicked_ratio": ratios["clicked_ratio"],
        "opened_ratio": ratios["opened_ratio"],
        "submitted_ratio": ratios["submitted_ratio"],
        "reported_ratio": ratios["reported_ratio"],
    }
    return ret_val

def get_related_subscription_stats(subscription,start_date):
    """
    Get base stats for all related subscriptions (national, sector, industry, and customer)
    """
    # Get the customer associated with the subscription
    _customer = get_single(
        subscription["customer_uuid"],"customer",CustomerModel,validate_customer            
    )

    
    # Get a list of all customers with the same sector so sector/industry averages can be calculated 
    parameters = {"sector": _customer['sector']}
    fields = { 
        "customer_uuid": 1, 
        "sector": 1,
        "industry": 1,
        }
    customer_list_by_sector = get_list(
        parameters, "customer", TestModel, validate_test, fields
    )

    sector_customer_uuids = []
    industry_customer_uuids = []
    # sector_customer_uuids = customer_list_by_sector
    # industry_customer_uuids = list(filter(lambda x: x["industry"] ==_customer["industry"], customer_list_by_sector))
    for cust in customer_list_by_sector:
        sector_customer_uuids.append(cust["customer_uuid"])
        if cust["industry"] == _customer["industry"]:
            industry_customer_uuids.append(cust["customer_uuid"])
    

    parameters = {
        "active": True,
    }
    subscription_fields = { 
        "customer_uuid": 1, 
        "subscription_uuid": 1,
        "cycles": 1,
        "name" : 1
    }
    subscription_list = get_list(
        parameters, "subscription", SubscriptionModel, validate_subscription, subscription_fields
    )

    sector_subscriptions = []
    industry_subscriptions = []
    customer_subscriptions = []

    sector_subscriptions = list(filter(lambda x: x["customer_uuid"] in sector_customer_uuids, subscription_list))
    industry_subscriptions = list(filter(lambda x: x["customer_uuid"] in industry_customer_uuids, subscription_list))
    customer_subscriptions = list(filter(lambda x: x["customer_uuid"] == _customer["customer_uuid"], subscription_list))

    #Generate region stats, use all cycles. Get cycle specific query for customer data
    national_stats = generate_region_stats(subscription_list)
    sector_stats = generate_region_stats(sector_subscriptions)
    industry_stats = generate_region_stats(industry_subscriptions)
    customer_stats = generate_region_stats(customer_subscriptions,start_date)
    
    return {
        "national" : national_stats,
        "sector" : sector_stats,
        "industry" : industry_stats,
        "customer" : customer_stats
    }

def get_cycles_breakdown(cycles):
    """
    Get a breakdown of all cycles for a given subscription
    """
    cycle_stats = []
    for cycle in cycles:
        cycle_stats.append({
            "ratios": calc_ratios(cycle["phish_results"]),
            "start_date": cycle["start_date"],
            "end_date": cycle["end_date"],            
            })
    return cycle_stats

def get_statistic_from_group(subscription_stats,deception_level,category,stat):
    """
    Get a specific stat if it exists off of the subscription stats consolidation
    Stats : Average, Count, Maximum, Median, Minimum

    """
    try: 
        return subscription_stats[deception_level][category][stat]
    except:
        return None

def get_reports_to_click(subscription_stats):
    """
    Helper function to get reports to click ratio, ensuring division by zero does not happen
    """
    try:
        return subscription_stats["stats_all"]["reported"]["count"] / subscription_stats["stats_all"]["clicked"]["count"]
    except:
        return None



def get_most_successful_campaigns(subscription_stats,category):
    """
    Get a list of the most succesful campaigns by a given category (submitted, opened, clicked, reported)

    Returns a list of the most succesful campagins. Will typically only return one but a 
    list is used in case of a tie in the provided category values.
    """
    category_ratio = f"{category}_ratio"
    most_succesful_campaigns = []
    for campaign in subscription_stats["campaign_results"]:
        if not most_succesful_campaigns:
            if campaign["ratios"][category_ratio]:
                most_succesful_campaigns.append(campaign)
        else:
            for current_campaign in most_succesful_campaigns:
                if campaign["ratios"][category_ratio]:
                    if campaign["ratios"][category_ratio] > current_campaign["ratios"][category_ratio]:
                        most_succesful_campaigns = []
                        most_succesful_campaigns.append(campaign)
    return most_succesful_campaigns

def campaign_templates_to_string(most_succesful_campaigns):
    """
    Given a list of campaigns, create a display string using there names
    """
    ret_string = ""
    for campaign in most_succesful_campaigns:
         ret_string += f"Level {campaign['deception_level']} \"{campaign['template_name']}\""
    return ret_string

def get_template_details(campaign_results):
    parameters = {}
    fields = { 
        "template_uuid": 1, 
        "name": 1,
        "deception_score": 1,
        "description": 1,
        "appearance": 1,
        "sender": 1,
        "relevancy": 1,
        "behavior": 1
        }
    template_list = get_list(
        parameters, "template", TemplateModel, validate_template, fields
    )
    
    # Possible large performance hit here. Break out repository to use built in mongo $in functionallity to fix
    for template in template_list:
        for campaign in campaign_results:
            if campaign["template_uuid"] == template["template_uuid"]:
                campaign["template_details"] = {}
                for key in template:
                    campaign["template_details"][key] = template[key]
    
    

