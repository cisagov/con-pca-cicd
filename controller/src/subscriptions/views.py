import requests
from datetime import datetime

from django.shortcuts import render

from .manager import SubscriptionManager


def subscribe(request, new_context={}):
    """ This handles a couple of postbacks, SUBMIT and DELETE """
    context = {}
    context.update(new_context)

    # handle submit request
    if 'submit_campaign' in request.POST:
        man = SubscriptionManager()
        man.create_gophish_campaign_request(request)
        context = { 'instant_msg': 'A new campaign was submitted' }

    # handle delete request
    if 'delete_all' in request.POST:
        man = SubscriptionManager()
        man.delete_all_groups()
        man.delete_all_campaigns()
        context = { 'instant_msg': 'Everything has been deleted' }

    return render(request, 'subscriptions/subscribe.html', context)


def view_campaigns(request):
    """ view a list of campaigns """
    man = SubscriptionManager()
    campaigns = man.get_campaigns()

    # add a true datetime attribute for display filter
    for c in campaigns:
        c.created_date = fix_date(c.created_date)
        try:
            # if the fractional seconds is more than 6 decimal places, this will throw an exception 
            c.created_date_dt = datetime.strptime(c.created_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        except:
            print('!!!! exception trying to parse ' + c.created_date)
            c.created_date_dt = datetime.now()

    context = { 'campaigns': campaigns }
    return render(request, 'subscriptions/campaigns.html', context)


def dhl_view(request):
    return render(request, 'emails/dhl.html')

# # TODO: Move this to a central 'utilities' module
# def fix_date(date_string):
#         pieces = parse('{a}.{f}Z', date_string)
#         f = pieces.named['f']
#         if len(f) > 6:
#             f = f[0:6]

#         return pieces.named['a'] + '.' + str(f) + 'Z'
