"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
import logging

# Local Libraries
from api.manager import CampaignManager, TemplateManager
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.subscriptions_serializers import (
    SubscriptionDeleteResponseSerializer,
    SubscriptionGetSerializer,
    SubscriptionPatchResponseSerializer,
    SubscriptionPatchSerializer,
    SubscriptionPostResponseSerializer,
    SubscriptionPostSerializer,
)
from api.utils.db_utils import (
    delete_single,
    get_list,
    get_single,
    update_single,
)

from api.utils import subscription_utils

# Third Party Libraries
from drf_yasg import openapi
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
        manual_parameters=[
            openapi.Parameter(
                "archived",
                openapi.IN_QUERY,
                description="Show archived subscriptions",
                type=openapi.TYPE_BOOLEAN,
                default=False,
            ),
            openapi.Parameter(
                "template",
                openapi.IN_QUERY,
                description="Show only subscriptions that are using a template",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request):
        """Get method."""
        parameters = {"archived": {"$in": [False, None]}}

        archivedParm = request.GET.get("archived")
        if archivedParm:
            if archivedParm.lower() == "true":
                parameters["archived"] = True

        if request.GET.get("template"):
            parameters["templates_selected_uuid_list"] = request.GET.get("template")

        subscription_list = get_list(
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

        created_response = subscription_utils.start_subscription(data=post_data)

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Get a Substription with subscription_uuid.
    """

    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get single Subscription",
        operation_description="This handles the API for the Get a Subscription with subscription_uuid.",
    )
    def get(self, request, subscription_uuid):
        """Get method."""
        print("get subscription_uuid {}".format(subscription_uuid))
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
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
        logger.debug("update subscription_uuid {}".format(subscription_uuid))
        put_data = request.data.copy()
        serialized_data = SubscriptionPatchSerializer(put_data)
        updated_response = update_single(
            uuid=subscription_uuid,
            put_data=serialized_data.data,
            collection="subscription",
            model=SubscriptionModel,
            validation_model=validate_subscription,
        )
        logger.info("created response {}".format(updated_response))
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
        """Delete method."""
        logger.debug("delete subscription_uuid {}".format(subscription_uuid))

        subscription = get_single(
            uuid=subscription_uuid,
            collection="subscription",
            model=SubscriptionModel,
            validation_model=validate_subscription,
        )

        # Delete campaigns
        groups_to_delete = set()
        for campaign in subscription["gophish_campaign_list"]:
            for group in campaign["groups"]:
                if group["id"] not in groups_to_delete:
                    groups_to_delete.add(group["id"])
            for id in groups_to_delete:
                try:
                    campaign_manager.delete("user_group", group_id=id)
                except Exception as error:
                    print("failed to delete group: {}".format(error))
            # Delete Templates
            campaign_manager.delete(
                "email_template", template_id=campaign["email_template_id"]
            )
            # Delete Campaigns
            campaign_manager.delete("campaign", campaign_id=campaign["campaign_id"])
        # Delete Groups
        for group_id in groups_to_delete:
            campaign_manager.delete("user_group", group_id=group_id)

        # Remove from the scheduler
        if subscription["task_uuid"]:
            revoke(subscription["task_uuid"], terminate=True)

        delete_response = delete_single(
            uuid=subscription_uuid,
            collection="subscription",
            model=SubscriptionModel,
            validation_model=validate_subscription,
        )

        logger.info("delete responce {}".format(delete_response))
        if "errors" in delete_response:
            return Response(delete_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionDeleteResponseSerializer(delete_response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionsCustomerListView(APIView):
    """
    This is the SubscriptionsCustomerListView APIView.

    This handles the API to get a List of Subscriptions with customer_uuid.
    """

    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get list of Subscriptions via customer_uuid",
        operation_description="This handles the API for the Get a Substription with customer_uuid.",
    )
    def get(self, request, customer_uuid):
        """Get method."""
        parameters = {"customer_uuid": customer_uuid, "archived": False}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        serializer = SubscriptionGetSerializer(subscription_list, many=True)
        return Response(serializer.data)


class SubscriptionsTemplateListView(APIView):
    """
    This is the SubscriptionsTemplateListView APIView.

    This handles the API to get a list of subscriptions by template_uuid
    """

    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get list of subscriptions via template_uuid",
        operation_description="This handles the API fro the get a subscription with template_uuid",
    )
    def get(self, request, template_uuid):
        """Get method."""
        parameters = {"templates_selected_uuid_list": template_uuid, "archived": False}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        serializer = SubscriptionGetSerializer(subscription_list, many=True)
        return Response(serializer.data)


class SubscriptionStopView(APIView):
    """
    This is the SubscriptionStopView APIView.

    This handles the API to stop a Subscription using subscription_uuid.
    """

    @swagger_auto_schema(
        responses={"202": SubscriptionPatchResponseSerializer, "400": "Bad Request"},
        operation_id="Endpoint for manually stopping a subscription",
        operation_description="Endpoint for manually stopping a subscription",
    )
    def get(self, request, subscription_uuid):
        """Get method."""
        # get subscription
        subscription = get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )

        # Stop subscription
        resp = subscription_utils.stop_subscription(subscription)

        # Cancel scheduled subscription emails
        if subscription["task_uuid"]:
            revoke(subscription["task_uuid"], terminate=True)

        # Return updated subscriptions
        serializer = SubscriptionPatchResponseSerializer(resp)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class SubscriptionRestartView(APIView):
    """
    This is the SubscriptionRestartView APIView.
    This handles the API to restart a Subscription
    """

    @swagger_auto_schema(
        responses={"201": SubscriptionPostResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Restart Subscription",
        operation_description="Endpoint for manually restart a subscription",
    )
    def get(self, request, subscription_uuid):
        created_response = subscription_utils.start_subscription(
            subscription_uuid=subscription_uuid
        )
        # Return updated subscription
        serializer = SubscriptionPatchResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
