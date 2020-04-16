import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.manager import CampaignManager
from api.serializers import campaign_serializers

logger = logging.getLogger(__name__)
manager = CampaignManager()


class CampaignListView(APIView):
    """
    This is the a Campaign list API View.

    This handles the API to get a List of GoPhish Campaigns.
    """

    def get(self, request):
        campaigns = manager.get("campaign")
        serializer = campaign_serializers.CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


class CampaignDetailView(APIView):
    """
    This is the Campaign Detail APIView.

    This handles the API to get Campaign details with campaign_id from GoPhish.
    """

    def get(self, request, campaign_id):
        campaign = manager.get("campaign", campaign_id=campaign_id)
        serializer = campaign_serializers.CampaignSerializer(campaign)
        return Response(serializer.data)
