"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
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

        # Get all templates for calc
        template_list = get_list(None, "template", TemplateModel, validate_template)

        template_data = {
            i.get("template_uuid"): i.get("descriptive_words") for i in template_list
        }

        # Data for Template calculation ToDo: Save relevant_templates
        url = post_data.get("url")
        keywords = post_data.get("keywords")
        relevant_templates = template_manager.get_templates(
            url, keywords, template_data
        )[:15]

        # Return 15 of the most relevant templates
        post_data["templates_selected_uuid_list"] = relevant_templates

        # get customer data
        customer = get_single(
            post_data["customer_uuid"], "customer", CustomerModel, validate_customer
        )

        # get relevent template data
        template_list = [
            x for x in template_list if x["template_uuid"] in relevant_templates
        ]
        templates = personalize_template(customer, template_list, post_data)

        # Data for GoPhish
        first_name = post_data.get("primary_contact").get("first_name", "")
        last_name = post_data.get("primary_contact").get("last_name", "")

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
            # Create new template
            created_template = campaign_manager.generate_email_template(
                name=template["name"], template=template["data"]
            )

            if created_template is not None:
                template_name = created_template.name
                campaign_name = f"{first_name}.{last_name}.1.1 {template_name}"
                campaign = campaign_manager.create(
                    "campaign",
                    campaign_name=campaign_name,
                    smtp_name="SMTP",
                    page_name="Phished",
                    user_group=target,
                    email_template=created_template,
                )
                logger.info("campaign created: {}".format(campaign))

                created_campaign = {
                    "campaign_id": campaign.id,
                    "name": campaign_name,
                    "created_date": format_ztime(campaign.created_date),
                    "launch_date": format_ztime(campaign.launch_date),
                    "email_template": created_template.name,
                    "landing_page_template": campaign.page.name,
                    "status": campaign.status,
                    "results": [],
                    "groups": [],
                    "timeline": [
                        {
                            "email": None,
                            "time": format_ztime(campaign.created_date),
                            "message": "Campaign Created",
                            "details": "",
                        }
                    ],
                    "target_email_list": target_list,
                }
                gophish_campaign_list.append(created_campaign)

        post_data["gophish_campaign_list"] = gophish_campaign_list

        created_response = save_single(
            post_data, "subscription", SubscriptionModel, validate_subscription
        )

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
        operation_description="This handles the API for the Get a Substription with subscription_uuid.",
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
        logger.info("created responce {}".format(updated_response))
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
        parameters = {"customer_uuid": customer_uuid}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        serializer = SubscriptionGetSerializer(subscription_list, many=True)
        return Response(serializer.data)
