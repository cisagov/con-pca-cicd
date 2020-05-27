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
from api.utils.subscription_utils import get_campaign_dates, target_list_divide
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

        # Data for Template calculation
        if post_data.get("keywords"):
            relevant_templates = template_manager.get_templates(
                post_data.get("url"), post_data.get("keywords"), template_data
            )[:15]
        else:
            relevant_templates = []

        divided_templates = [
            relevant_templates[x : x + 5] for x in range(0, len(relevant_templates), 5)
        ]

        # Get the next date Intervals
        start_date = post_data.get("start_date")
        campaign_data_list = get_campaign_dates(start_date)

        # Return 15 of the most relevant templates
        post_data["templates_selected_uuid_list"] = relevant_templates
        # get customer data
        customer = get_single(
            post_data["customer_uuid"], "customer", CustomerModel, validate_customer
        )

        template_personalized_list = []
        for template_group in divided_templates:
            template_data_list = [
                x for x in template_list if x["template_uuid"] in template_group
            ]
            templates = personalize_template(customer, template_data_list, post_data)
            template_personalized_list.append(templates)

        # divide emails, TODO: replace with this random email picker
        target_list = post_data.get("target_email_list")
        target_div = target_list_divide(target_list)
        index = 0
        for campaign_info in campaign_data_list:
            campaign_info["templetes"] = template_personalized_list[index]
            campaign_info["targets"] = target_div[index]
            index += 1

        # Data for GoPhish
        first_name = post_data.get("primary_contact").get("first_name", "")
        last_name = post_data.get("primary_contact").get("last_name", "")
        # get User Groups
        user_groups = campaign_manager.get("user_group")

        # create campaigns
        group_number = 0
        for campaign_info in campaign_data_list:
            campaign_group = f"{first_name}.{last_name}.1.1 Targets.{group_number} "
            group_number += 1
            if campaign_group not in [group.name for group in user_groups]:
                target_group = campaign_manager.create(
                    "user_group",
                    group_name=campaign_group,
                    target_list=campaign_info["targets"],
                )
            else:
                # get group from list
                for user_group in user_groups:
                    if user_group.name == campaign_group:
                        target_group = user_group
                        break

            gophish_campaign_list = self.__create_and_save_campaigns(
                campaign_info, target_group, first_name, last_name
            )

        post_data["gophish_campaign_list"] = gophish_campaign_list

        created_response = save_single(
            post_data, "subscription", SubscriptionModel, validate_subscription
        )

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __create_and_save_campaigns(
        self, campaign_info, target_group, first_name, last_name
    ):
        """
        Create and Save Campaigns.

        This method handles the creation of each campain with given template, target group, and data.
        """
        templates = campaign_info["templetes"]
        targets = campaign_info["targets"]

        gophish_campaign_list = []
        # Create a GoPhish Campaigns
        for template in templates:
            # Create new template
            created_template = campaign_manager.generate_email_template(
                name=template["name"], template=template["data"]
            )
            campaign_start = campaign_info["start_date"].strftime("%Y-%m-%d")
            campaign_end = campaign_info["send_by_date"].strftime("%Y-%m-%d")

            if created_template is not None:
                template_name = created_template.name
                campaign_name = f"{first_name}.{last_name}.1.1 {template_name} {campaign_start}-{campaign_end}"
                print(campaign_info["start_date"])
                campaign = campaign_manager.create(
                    "campaign",
                    campaign_name=campaign_name,
                    smtp_name="SMTP",
                    page_name="Phished",
                    user_group=target_group,
                    email_template=created_template,
                    launch_date=campaign_info["start_date"].strftime(
                        "%Y-%m-%dT%H:%M:%S+00:00"
                    ),
                    send_by_date=campaign_info["send_by_date"].strftime(
                        "%Y-%m-%dT%H:%M:%S+00:00"
                    ),
                )
                logger.info("campaign created: {}".format(campaign))
                created_campaign = {
                    "campaign_id": campaign.id,
                    "name": campaign_name,
                    "created_date": format_ztime(campaign.created_date),
                    "launch_date": campaign_info["start_date"],
                    "send_by_date": campaign_info["send_by_date"],
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
                    "target_email_list": targets,
                }
                gophish_campaign_list.append(created_campaign)

        return gophish_campaign_list


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
        logging.info("created response {}".format(updated_response))
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
        logging.info("delete response {}".format(delete_response))
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


class SubscriptionsTemplateListView(APIView):
    """
    This is the SubscriptionsTemplateListView APIView.

    This handles the API to get a list of subscriptions by template_uuid
    """
    @swagger_auto_schema(
        responses={"200": SubscriptionGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get list of subscriptions via template_uuid",
        operation_description="This handles the API fro the get a subscription with template_uuid"
    )
    def get(self, request, template_uuid):
        """Get method."""
        parameters = {"templates_selected_uuid_list": template_uuid}
        subscription_list = get_list(
            parameters, "subscription", SubscriptionModel, validate_subscription
        )
        serializer = SubscriptionGetSerializer(subscription_list, many=True)
        return Response(serializer.data)
