import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.manager import CampaignManager


logger = logging.getLogger(__name__)
manager = CampaignManager()


class CampaignListView(APIView):
    """
    This is the a Campaign list API View.

    This handles the API to get a List of GoPhish Campaigns.
    """

    def get(self, request):
        campaigns = manager.get("campaign")
        context = {
            campaign.id: {
                "name": campaign.name,
                "created date": campaign.created_date,
                "send by date": campaign.send_by_date,
                "launch date": campaign.launch_date,
                "status": campaign.status,
            }
            for campaign in campaigns
        }
        return Response(context)


class CampaignView(APIView):
    """
    This is the Campaign Detail APIView.

    This handles the API to get Campaign details with campaign_id from GoPhish.
    """

    def get(self, request, campaign_id):
        campaign = manager.get("campaign", campaign_id=campaign_id)

        context = {
            "id": campaign.id,
            "name": campaign.name,
            "created date": campaign.created_date,
            "launch date": campaign.launch_date,
            "status": campaign.status,
        }

        return Response(context)
