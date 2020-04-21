"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
import asyncio
import datetime
import logging
import uuid

# Third-Party Libraries
# Local
from api.manager import CampaignManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.subscriptions_serializers import (
    SubscriptionGetSerializer,
    SubscriptionPostResponseSerializer,
    SubscriptionPostSerializer,
)
from api.utils import db_service
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# GoPhish API Manager
manager = CampaignManager()


class SubscriptionsListView(APIView):
    """
    This is the SubscriptionsListView APIView.

    This handles the API to get a List of Subscriptions.
    """

    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Subscriptions",
        operation_description="This handles the API to get a List of Subscriptions.",
    )
    def get(self, request):
        """Get method."""
        parameters = request.data.copy()
        subscription_list = self.__get_data(parameters)
        serializer = SubscriptionGetSerializer(subscription_list, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SubscriptionPostSerializer,
        responses={"201": SubscriptionPostResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Create Subscription",
        operation_description="This handles Creating a Subscription and launching a Campaign.",
    )
    def post(self, request, format=None):
        """Post method."""
        post_data = request.data.copy()

        # Data for GoPhish
        first_name = post_data.get("primary_contact").get("first_name", "")
        last_name = post_data.get("primary_contact").get("last_name", "")
        templates = manager.get("email_template")
        phish_url = "https://phish.hyreguard.com/"
        # Create a User Group
        existing_group_names = [group.name for group in manager.get("user_group")]
        group_name = f"{last_name}'s Targets"
        target_list = post_data.get("target_email_list")
        if group_name not in existing_group_names:
            target = manager.create(
                "user_group", group_name=group_name, target_list=target_list
            )
        else:
            target = manager.get("user_group")[0]

        gophish_campaign_list = []

        # Create a GoPhish Campaigns
        for template in templates:
            template_name = template.name
            campaign_name = f"{first_name}.{last_name}.1.1 {template_name}"
            campaign = manager.create(
                "campaign",
                campaign_name=campaign_name,
                user_group=target,
                email_template=template,
                phish_url=phish_url,
            )
            logger.info("campaign created: {}".format(campaign))
            created_campaign = {
                "name": campaign_name,
                "email_template": template.name,
                "landing_page_template": "",
                "target_email_list": target_list,
            }
            gophish_campaign_list.append(created_campaign)

        post_data["gophish_campaign_list"] = gophish_campaign_list

        created_response = self.__save_data(post_data)

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __get_data(self, parameters):
        """
        Get_data private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return subscription_list

    def __save_data(self, post_data):
        """
        Save_data private method.

        This method is a private method that takes in
        post_data and saves it to the db with the required feilds.
        ToDo: break out the email data into its own collection or keep flat as is.
        """
        create_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        post_data["subscription_uuid"] = str(uuid.uuid4())
        post_data["created_by"] = post_data["last_updated_by"] = current_user
        post_data["cb_timestamp"] = post_data["lub_timestamp"] = create_timestamp
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        created_responce = loop.run_until_complete(service.create(to_create=post_data))
        return created_responce


class SubscriptionView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Get a Substription with subscription_uuid.
    """

    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get single Subscription",
        operation_description="This handles the API for the Get a Substription with subscription_uuid.",
    )
    def get(self, request, subscription_uuid):
        """Get method."""
        print("get subscription_uuid {}".format(subscription_uuid))
        subscription = self.__get_single(subscription_uuid)
        serializer = SubscriptionGetSerializer(subscription)
        return Response(serializer.data)

    def __get_single(self, subscription_uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription = loop.run_until_complete(service.get(uuid=subscription_uuid))
        return subscription
