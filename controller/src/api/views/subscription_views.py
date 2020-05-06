"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
import asyncio
import datetime
import logging
import requests
import uuid

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
from api.serializers.subscriptions_serializers import (
    SubscriptionGetSerializer,
    SubscriptionPostResponseSerializer,
    SubscriptionPostSerializer,
    SubscriptionPatchResponseSerializer,
    SubscriptionPatchSerializer,
    SubscriptionDeleteResponseSerializer,
)
from api.utils import db_service
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# GoPhish API Manager
campaign_manager = CampaignManager()
# Template Calculator Manager
template_manager = TemplateManager()


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
        subscription_list = self.__get_data(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
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

        # Get all templates for calc
        template_list = self.__get_data(
            None, "template", TemplateModel, validate_template
        )

        template_data = {
            i.get("template_uuid"): i.get("descriptive_words") for i in template_list
        }

        # Data for Template calculation ToDo: Save relevant_templates
        relevant_templates = template_manager.get_templates(
            post_data.get("url"), post_data.get("keywords"), template_data
        )

        # Return 15 of the most relevant templates
        post_data["templates_selected_uuid_list"] = relevant_templates[:15]

        # Data for GoPhish
        first_name = post_data.get("primary_contact").get("first_name", "")
        last_name = post_data.get("primary_contact").get("last_name", "")
        templates = campaign_manager.get("email_template")
        # get User Groups
        user_groups = campaign_manager.get("user_group")
        group_name = f"{last_name}'s Targets"
        target_list = post_data.get("target_email_list")

        # Note: this could be refactored later
        if group_name not in [group.name for group in user_groups]:
            target = campaign_manager.create(
                "user_group", group_name=group_name, target_list=target_list
            )
        else:
            # get group from list
            for user_group in user_groups:
                if user_group.name == group_name:
                    target = user_group
                    break

        gophish_campaign_list = []

        # Create a GoPhish Campaigns
        for template in templates:
            template_name = template.name
            campaign_name = f"{first_name}.{last_name}.1.1 {template_name}"
            campaign = campaign_manager.create(
                "campaign",
                campaign_name=campaign_name,
                user_group=target,
                email_template=template,
            )
            logger.info("campaign created: {}".format(campaign))
            created_campaign = {
                "campaign_id": campaign.id,
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

    def __get_data(self, parameters, collection, model, validation_model):
        """
        Get_data private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service(collection, model, validation_model)
        document_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return document_list

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
        created_response = loop.run_until_complete(service.create(to_create=post_data))
        return created_response


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

    @swagger_auto_schema(
        request_body=SubscriptionPatchSerializer,
        responses={"202": SubscriptionPatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Update and Patch single subscription",
        operation_description="This handles the API for the Update subscription with subscription_uuid.",
    )
    def patch(self, request, subscription_uuid):
        """Patch method."""
        logging.debug("update subscription_uuid {}".format(subscription_uuid))
        put_data = request.data.copy()
        serialized_data = SubscriptionPatchSerializer(put_data)
        updated_response = self.__update_single(
            uuid=subscription_uuid, put_data=serialized_data.data
        )
        logging.info("created responce {}".format(updated_response))
        if "errors" in updated_response:
            return Response(updated_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPatchResponseSerializer(updated_response)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(
        responses={"200": SubscriptionDeleteResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Delete single subscription",
        operation_description="This handles the API for the Delete of a  subscription with subscription_uuid.",
    )
    def delete(self, request, subscription_uuid):
        """delete method."""
        logging.debug("delete subscription_uuid {}".format(subscription_uuid))
        delete_response = self.__delete_single(subscription_uuid)
        logging.info("delete responce {}".format(delete_response))
        if "errors" in delete_response:
            return Response(delete_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionDeleteResponseSerializer(delete_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def __update_single(self, uuid, put_data):
        """
        Update_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)

        updated_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        put_data["subscription_uuid"] = uuid
        put_data["last_updated_by"] = current_user
        put_data["lub_timestamp"] = updated_timestamp

        subscription = loop.run_until_complete(service.get(uuid=uuid))
        subscription.update(put_data)
        update_response = loop.run_until_complete(service.update(subscription))
        if "errors" in update_response:
            return update_response
        return subscription

    def __delete_single(self, uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)

        delete_response = loop.run_until_complete(service.delete(uuid=uuid))
        return delete_response
