"""Subscription Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta

# Third-Party Libraries
from lcgit import lcg


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
