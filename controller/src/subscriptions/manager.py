import requests
import datetime

from gophish import Gophish
from gophish.models import *

from django.template.loader import get_template


class SubscriptionManager():

    gp_url = 'https://gophish:3333'
    api_key = 'de618ad717bb478c84a0eae02faa64eaad4b3ec9b3f4b6b8ce7f131efb110fb6'


    def get_gophish(self):
        """ A wrapper to get a Gophish instance for our server. """
        return Gophish(self.api_key, host=self.gp_url, verify=False)

    def create_gophish_campaign_request(self, request):
        """ Take the posted values out of the request, formulate a BSON/JSON thing and push it to GoPhish
        sending get request and saving the response as response object
        """
        api = self.get_gophish()

        # build a brand new group
        group_name = 'group_' + request.POST['subscriber_name']

        # we are assuming up to 2 emails
        targets = []
        for x in range(1, 3):   
            if request.POST['first' + str(x)] != '':
                user = User(
                    first_name=request.POST['first' + str(x)],
                    last_name=request.POST['last' + str(x)],
                    email=request.POST['email' + str(x)],
                    position=request.POST['position' + str(x)],
                )
                targets.append(user)

        group = Group(name=group_name, targets=targets)
        api.groups.post(group)

        # build and post the campaign
        campaign_start = request.POST['campaign_start']
        if campaign_start == '':
            campaign_start = '01-01-0001'        
        launch_date = datetime.strptime(campaign_start, '%m-%d-%Y').strftime("%Y-%m-%dT12:00:00Z")

        campaign_end = request.POST['campaign_end']
        if campaign_end == '':
            campaign_end = campaign_start
        send_by_date = datetime.strptime(campaign_end, '%m-%d-%Y').strftime("%Y-%m-%dT12:00:00Z")

        groups = [group]
        template = get_template('emails/dhl.html')
        page = Page(name='jetsons_page')
        smtp = SMTP(name='jetsons_profile')
        #url = 'http://csetac.inl.gov:3333'

        campaign = Campaign(
            name='Test Campaign - ' + request.POST['subscriber_name'], 
            launch_date=launch_date,
            send_by_date=send_by_date,
            groups=groups, 
            page=page,
            template=template, 
            smtp=smtp)

        campaign = api.campaigns.post(campaign)


    
    def get_campaigns(self):
        """ Returns campaign summaries """
        api = self.get_gophish()
        return api.campaigns.get()



    def get_groups(self):
        api = self.get_gophish()

        for group in api.groups.get():
            print('{} has {} users'.format(group.name, len(group.targets)))

        group_1 = api.groups.get(group_id=1)
        print(repr(group_1))



    def delete_all_groups(self):
        """ Convenience method for clean up during development """
        api = self.get_gophish()

        for group in api.groups.get():
            api.groups.delete(group.id)



    def delete_all_campaigns(self):
        """ Convenience method for cleanup during development """
        api = self.get_gophish()

        for campaign in api.campaigns.get():
            api.campaigns.delete(campaign.id)
