"""
Sending Profile Views.
This handles the api for all the Sending Profile urls.
"""
# Standard Python Libraries
import logging
# Third-Party Libraries
# Local
from api.manager import CampaignManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
from api.serializers.sendingprofile_serializers import (
    SendingProfileSerializer, SendingProfilePatchSerializer, SendingProfilePatchResponseSerializer
)
from api.utils.db_utils import (
    delete_single,
    get_list,
    get_single,
    save_single,
    update_single,
)
from api.utils.template_utils import format_ztime, personalize_template
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
logger = logging.getLogger(__name__)
# GoPhish API Manager
campaign_manager = CampaignManager()

class SendingProfilesListView(APIView):
    """
    This is the SendingProfilesListView APIView.
    This handles the API to get a List of Sending Profiles.
    """
    @swagger_auto_schema(
        responses={"200": SendingProfileSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Sending Profiles",
        operation_description="This handles the API to get a List of Sending Profiles.",
    )
    def get(self, request):
        """Get method."""
        sending_profiles = campaign_manager.get("sending_profile")
        serializer = SendingProfileSerializer(sending_profiles, many=True)
        return Response(serializer.data)

    """
    This is the SendingProfileView APIView.
    This handles the API for creating a new Sending Profile.
    https://localhost:3333/api/smtp/:id
    """
    @swagger_auto_schema(
        request_body=SendingProfilePatchSerializer,
        responses={"202": SendingProfilePatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Create Sending Profile",
        operation_description="This handles the API for the Update Sending Profile with uuid.",
    )
    def post(self, request):
        sp = request.data.copy()
        sending_profile = campaign_manager.create(
            "sending_profile", 
            name=sp.get("name"),
            username=sp.get("username"),
            password=sp.get("password"),
            host=sp.get("host"),
            interface_type=sp.get("interface_type"),
            from_address=sp.get("from_address"),
            ignore_cert_errors=sp.get("ignore_cert_errors"),
            headers=sp.get("headers")
        )
        serializer = SendingProfileSerializer(sending_profile)
        return Response(serializer.data)


class SendingProfileView(APIView):
    """
    This is the SendingProfileView APIView.
    This handles the API for the Get a Sending Profile with id.
    """
    @swagger_auto_schema(
        responses={"200": SendingProfileSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get single Sending Profile",
        operation_description="This handles the API for the Get a Sending Profile with id.",
    )
    def get(self, request, id):
        sending_profile = campaign_manager.get("sending_profile", smtp_id=id)
        serializer = SendingProfileSerializer(sending_profile)
        return Response(serializer.data)


    """
    This is the SendingProfileView APIView.
    This handles the API for PATCHing a Sending Profile with id.
    https://localhost:3333/api/smtp/:id
    """
    @swagger_auto_schema(
        request_body=SendingProfilePatchSerializer,
        responses={"202": SendingProfilePatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Update and Patch single Sending Profile",
        operation_description="This handles the API for the Update Sending Profile with uuid.",
    )
    def patch(self, request, id):
        # get the saved record
        sending_profile = campaign_manager.get("sending_profile", smtp_id=id)

        # patch the supplied data
        # .....


        # get the new version to make sure we return the latest
        sending_profile = campaign_manager.get("sending_profile", smtp_id=id)
        serializer = SendingProfileSerializer(sending_profile)
        return Response(serializer.data)


