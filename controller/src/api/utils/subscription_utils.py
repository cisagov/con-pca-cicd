"""Subscription Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta


def get_campaign_dates(start_date_string):
    """
    Get Campaign Dates.

    Using given start date,
    genereate the 3 campaign dates in 30 days increments.
    """
    start_date = datetime.strptime(
        start_date_string, "%Y-%m-%dT%H:%M:%S"
    )  # Format inbound 2020-03-10T09:30:25
    thirty_days = timedelta(days=30)
    # your calculated date
    # start: start_date
    # 30 days later: start_date + thirty_days
    # 60 days later: 60_days + thirty_days
    # 90 end//: 90_days + 30
    thirty_days_later = start_date + thirty_days

    sixty_days_later = thirty_days_later + thirty_days

    ninety_days_later = sixty_days_later + thirty_days

    return_list = []

    return_list.append(
        {
            "start_date": start_date,
            "send_by_date": thirty_days_later,
            "templetes": [],
            "targets": [],
        }
    )
    return_list.append(
        {
            "start_date": thirty_days_later,
            "send_by_date": sixty_days_later,
            "templetes": [],
            "targets": [],
        }
    )
    return_list.append(
        {
            "start_date": sixty_days_later,
            "send_by_date": ninety_days_later,
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
    avg = len(target_list) / float(3)
    return_lists = []
    last = 0.0

    while last < len(target_list):
        return_lists.append(target_list[int(last) : int(last + avg)])
        last += avg

    return return_lists
