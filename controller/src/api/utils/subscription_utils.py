"""Subscription Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta

# Third-Party Libraries
from lcgit import lcg

from api.serializers.subscriptions_serializers import SubscriptionPatchSerializer
from api.models.subscription_models import SubscriptionModel, validate_subscription

from api.manager import CampaignManager

from api.utils import db_utils

campaign_manager = CampaignManager()


def get_campaign_dates(start_date_string):
    """
    Get Campaign Dates.

    Using given start date,
    genereate the 3 campaign dates in 30 days increments.
    """
    start_date = datetime.strptime(
        start_date_string, "%Y-%m-%dT%H:%M:%S"
    )  # Format inbound 2020-03-10T09:30:25
    sixty_days = timedelta(days=60)
    # your calculated date
    # start: start_date
    # 60 days later: start_date + 60_days
    # send all at once, send by 60 days, end at 90
    sixty_days_later = start_date + sixty_days
    return_list = []

    return_list.append(
        {
            "start_date": start_date,
            "send_by_date": sixty_days_later,
            "templetes": [],
            "targets": [],
        }
    )
    return_list.append(
        {
            "start_date": start_date,
            "send_by_date": sixty_days_later,
            "templetes": [],
            "targets": [],
        }
    )
    return_list.append(
        {
            "start_date": start_date,
            "send_by_date": sixty_days_later,
            "templetes": [],
            "targets": [],
        }
    )
    return return_list


def target_list_divide(target_list):
    """
    Target List Divide.

    Temp funtion to divide list of targets into 3 sub lists.
    ToDo: replace with random selecter algorithm.
    """
    target_list = lcgit_list_randomizer(target_list)
    avg = len(target_list) / float(3)
    return_lists = []
    last = 0.0

    while last < len(target_list):
        return_lists.append(target_list[int(last) : int(last + avg)])
        last += avg

    return return_lists


def lcgit_list_randomizer(object_list):
    """
    Lcgit List Randomizer.

    This uses lcgit from https://github.com/cisagov/lcgit
    to genrate a random list order
    """
    random_list = []
    for item in lcg(object_list):
        random_list.append(item)
    return random_list


def stop_subscription(subscription):
    """
    Stops a given subscription.

    Returns updated subscription.
    """

    def stop_campaign(campaign):
        """
        Stops a given campaign.

        Returns updated Campaign
        """
        campaign_manager.complete_campaign(campaign_id=campaign['campaign_id'])
        campaign['status'] = 'stopped'
        campaign['completed_date'] = datetime.now()
        return campaign


    # Stop Campaigns
    updated_campaigns = list(map(stop_campaign, subscription['gophish_campaign_list']))
    
    # TODO: Remove from scheduler

    # Update subscription
    subscription['gophish_campaign_list'] = updated_campaigns
    subscription['active'] = False
    subscription['manually_stopped'] = True
    subscription['status'] = 'stopped'
    resp = db_utils.update_single(
        uuid=subscription['subscription_uuid'],
        put_data=SubscriptionPatchSerializer(subscription).data,
        collection="subscription",
        model=SubscriptionModel,
        validation_model=validate_subscription
    )

    return resp



