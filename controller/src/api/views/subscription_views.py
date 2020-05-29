"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
from datetime import datetime
import logging

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import TemplateModel, validate_template
from api.serializers import campaign_serializers
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

from api.utils import subscription_utils

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

        # get customer data
        customer = get_single(
            post_data["customer_uuid"], "customer", CustomerModel, validate_customer
        )

        #Get list of all subscriptions for incrementing sub name
        customer_filter = {'customer_uuid': post_data["customer_uuid"]}
        subscription_list = get_list(
            customer_filter, "subscription", SubscriptionModel, validate_subscription
        )
        increment_position = 4 #The position the individual subscriptions is being counted from
        
        previous_incrments = []
        for sub in subscription_list:
            previous_incrments.append(sub['name'].split(".")[increment_position])
        
        first_increment = 1 #Modify when the first increment value has a purpose determined
        second_increment = 1 if not previous_incrments else int(max(previous_incrments)) + 1

        # Generate sub name using customer and increment info
        post_data['name'] = f"{customer['identifier']}.{customer['contact_list'][0]['first_name']}.{customer['contact_list'][0]['last_name']}.{first_increment}.{second_increment}"


        # Get all Email templates for calc
        template_list = get_list(
            {"template_type": "Email"}, "template", TemplateModel, validate_template
        )

        # Get all Landning pages or defult
        # This is currently selecting the defult page on creation.
        # landing_template_list = get_list({"template_type": "Landing"}, "template", TemplateModel, validate_template)
        landing_page = "Phished"

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

        # Get the next date Intervals, if no startdate is sent, default today
        start_date = post_data.get(
            "start_date", datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        )
        campaign_data_list = get_campaign_dates(start_date)

        # Return 15 of the most relevant templates
        post_data["templates_selected_uuid_list"] = relevant_templates
        
        template_personalized_list = []
        for template_group in divided_templates:
            template_data_list = [
                x for x in template_list if x["template_uuid"] in template_group
            ]
            templates = personalize_template(customer, template_data_list, post_data)
            template_personalized_list.append(templates)

        # divide emails
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
        gophish_campaign_list = []
        for campaign_info in campaign_data_list:
            campaign_group = f"{post_data['name']}.Targets.{group_number} "
            campaign_info["name"] = f"{post_data['name']}.{group_number}"
            group_number += 1
            # if campaign_group not in [group.name for group in user_groups]:
            target_group = campaign_manager.create(
                "user_group",
                group_name=campaign_group,
                target_list=campaign_info["targets"],
            )
            # else:
            #     # get group from list
            #     for user_group in user_groups:
            #         if user_group.name == campaign_group:
            #             target_group = user_group
            #             break
            gophish_campaign_list.extend(self.__create_and_save_campaigns(
                campaign_info, target_group, first_name, last_name, landing_page
            ))

        post_data["gophish_campaign_list"] = gophish_campaign_list
        
        created_response = save_single(
            post_data, "subscription", SubscriptionModel, validate_subscription
        )

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __create_and_save_campaigns(
        self, campaign_info, target_group, first_name, last_name, landing_page
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
                if not campaign_info["name"]:
                    campaign_name = f"{first_name}.{last_name}.1.1 {template_name} {campaign_start}-{campaign_end}"
                else:
                    campaign_name = f"{campaign_info['name']}.{template_name}.{campaign_start}-{campaign_end}"
                print(campaign_info["start_date"])
                campaign = campaign_manager.create(
                    "campaign",
                    campaign_name=campaign_name,
                    smtp_name="SMTP",
                    page_name=landing_page,  # Replace with picked landing page, default init page now.
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
                    "email_template_id": created_template.id,
                    "landing_page_template": campaign.page.name,
                    "status": campaign.status,
                    "results": [],
                    "groups": [campaign_serializers.CampaignGroupSerializer(target_group).data],
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
        
        #Delete campaigns
        groups_to_delete = set()
        for campaign in subscription['gophish_campaign_list']:
            for group in campaign['groups']:
                if group['id'] not in groups_to_delete:
                    groups_to_delete.add(group['id'])
            for id in groups_to_delete:
                try:
                    group_del_result =  campaign_manager.delete("user_group",group_id=id)
                except:
                    print(f"failed to delete group ")
            # Delete Templates
            template_del_result = campaign_manager.delete("email_template",template_id=campaign["email_template_id"])
            # Delete Campaigns
            campaign_del_result = campaign_manager.delete("campaign", campaign_id=campaign['campaign_id'])
        # Delete Groups    
        for group_id in groups_to_delete:
            campaign_manager.delete("user_group", group_id=group_id)

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


class SubscriptionStopView(APIView):
    @swagger_auto_schema(
        responses={"202": SubscriptionPatchResponseSerializer, "400": "Bad Request"},
        operation_id="Endpoint for manually stopping a subscription",
        operation_description="Endpoint for manually stopping a subscription"
    )
    def get(self, request, subscription_uuid):

        # get subscription
        subscription = get_single(subscription_uuid, "subscription", SubscriptionModel, validate_subscription)
        
        # Stop subscription
        resp = subscription_utils.stop_subscription(subscription)

        # Return updated subscriptions
        serializer = SubscriptionPatchResponseSerializer(resp)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
