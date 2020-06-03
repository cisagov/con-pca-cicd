"""Subscription Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta

# Third-Party Libraries
# Local Libraries
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.subscriptions_serializers import SubscriptionPatchSerializer
from api.utils import db_utils
from celery.task.control import revoke
from lcgit import lcg

campaign_manager = CampaignManager()


def get_campaign_dates(start_date_string):
    """
    Get Campaign Dates.

    Using given start date,
    genereate the 3 campaign dates in 30 days increments.
    """
    try:
        start_date = datetime.strptime(
            start_date_string, "%Y-%m-%dT%H:%M:%S"
        )  # Format inbound 2020-03-10T09:30:25
    except Exception:
        start_date = datetime.strptime(
            start_date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
        )  # Format inbound 2020-03-10T09:30:25.227Z

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
        campaign_manager.complete_campaign(campaign_id=campaign["campaign_id"])
        campaign["status"] = "stopped"
        campaign["completed_date"] = datetime.now()
        return campaign

    # Stop Campaigns
    updated_campaigns = list(map(stop_campaign, subscription["gophish_campaign_list"]))

    # Remove from the scheduler
    revoke(subscription["task_uuid"], terminate=True)

    # Update subscription
    subscription["gophish_campaign_list"] = updated_campaigns
    subscription["active"] = False
    subscription["manually_stopped"] = True
    subscription["active_task"] = False
    subscription["status"] = "stopped"
    resp = db_utils.update_single(
        uuid=subscription["subscription_uuid"],
        put_data=SubscriptionPatchSerializer(subscription).data,
        collection="subscription",
        model=SubscriptionModel,
        validation_model=validate_subscription,
    )

    return resp


def get_sub_end_date(start_date_string):
    """
    Get Sub end date.

    Using given start date,
    generate the standered end_date 90 after start.
    """
    try:
        start_date = datetime.strptime(
            start_date_string, "%Y-%m-%dT%H:%M:%S"
        )  # Format inbound 2020-03-10T09:30:25
    except Exception:
        start_date = datetime.strptime(
            start_date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
        )  # Format inbound 2020-03-10T09:30:25.227Z
    ninety_days = timedelta(days=90)
    # your calculated date
    # start: start_date
    # 60 days later: start_date + 60_days
    # send all at once, send by 60 days, end at 90
    ninety_days_later = start_date + ninety_days
    return ninety_days_later
