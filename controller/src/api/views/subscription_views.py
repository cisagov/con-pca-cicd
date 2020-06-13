"""
Subscription Views.

This handles the api for all the Subscription urls.
"""
# Standard Python Libraries
from datetime import datetime
import logging
import json

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
from api.views.utils.subscription_utils import SubscriptionCreationManager
from api.models.customer_models import CustomerModel, validate_customer
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.models.template_models import (
    TagModel,
    TemplateModel,
    validate_tag,
    validate_template,
)
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
from api.utils.subscription_utils import (
    get_campaign_dates,
    get_sub_end_date,
    stop_subscription,
    target_list_divide,
)
from api.utils.template_utils import format_ztime, personalize_template
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from notifications.views import SubscriptionNotificationEmailSender
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
                parameters["archived"]["$in"].append(True)

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
        json.dumps(post_data)
        # get customer data
        customer = get_single(
            post_data["customer_uuid"], "customer", CustomerModel, validate_customer
        )

        # Get start date then quater of start date and create names to check
        start_date = post_data.get(
            "start_date", datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        )

        end_date = get_sub_end_date(start_date)
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        subscription_list = get_list(
            {"customer_uuid": post_data["customer_uuid"]},
            "subscription",
            SubscriptionModel,
            validate_subscription,
        )

        if len(subscription_list) == 0:
            # If no subscription was created, create first one:
            # {customer['identifier']}_1.1
            base_name = f"{customer['identifier']}_1.1"

        else:
            # Get all names, then split off the identifyers from name
            names = [x["name"] for x in subscription_list]
            list_tupe = []
            for name in names:
                int_ind, sub_id = name.split(".")
                _, sub = int_ind.split("_")
                list_tupe.append((sub, sub_id))
            # now sort tuple list by second element
            list_tupe.sort(key=lambda tup: tup[1])
            # get last run inc values
            last_ran_x, last_ran_y = list_tupe[-1]

            # now check to see there are any others running durring.
            active_subscriptions = [x for x in subscription_list if x["active"]]
            if len(active_subscriptions) <= 0:
                # if none are actvie, check last running number and create new name
                next_run_x, next_run_y = "1", str(int(last_ran_y) + 1)
            else:
                next_run_x, next_run_y = str(int(last_ran_x) + 1), last_ran_y

            base_name = f"{customer['identifier']}_{next_run_x}.{next_run_y}"

        # Generate sub name using customer and increment info
        post_data["name"] = base_name

        # Get all Email templates for calc
        email_template_params = {"template_type": "Email", "retired": False}
        template_list = get_list(
            email_template_params, "template", TemplateModel, validate_template
        )

        # Get all Landing pages or defult
        # This is currently selecting the default page on creation.
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

        print("divided_templates: {} items".format(len(divided_templates)))

        # Get the next date Intervals, if no startdate is sent, default today
        campaign_data_list = get_campaign_dates(start_date)

        # Return 15 of the most relevant templates
        post_data["templates_selected_uuid_list"] = relevant_templates

        template_personalized_list = []
        tag_list = get_list(None, "tag_definition", TagModel, validate_tag)
        for template_group in divided_templates:
            template_data_list = [
                x for x in template_list if x["template_uuid"] in template_group
            ]
            templates = personalize_template(
                customer, template_data_list, post_data, tag_list
            )
            template_personalized_list.append(templates)

        # divide emails
        target_list = post_data.get("target_email_list")
        target_div = target_list_divide(target_list)
        index = 0
        print(
            "template_personalized_list: {} items".format(
                len(template_personalized_list)
            )
        )
        for campaign_info in campaign_data_list:
            try:
                campaign_info["templates"] = template_personalized_list[index]
            except Exception as err:
                logger.info("error campaign_info templates {}".format(err))
                pass
            try:
                campaign_info["targets"] = target_div[index]
            except Exception as err:
                logger.info("error campaign_info targets {}".format(err))
                pass
            index += 1

        # Data for GoPhish
        # create campaigns
        group_number = 1
        gophish_campaign_list = []
        for campaign_info in campaign_data_list:
            campaign_group = f"{post_data['name']}.Targets.{group_number} "
            campaign_info["name"] = f"{post_data['name']}.{group_number}"
            group_number += 1
            target_group = campaign_manager.create(
                "user_group",
                group_name=campaign_group,
                target_list=campaign_info["targets"],
            )
            gophish_campaign_list.extend(
                self.__create_and_save_campaigns(
                    campaign_info, target_group, landing_page, end_date
                )
            )

        post_data["gophish_campaign_list"] = gophish_campaign_list
        # check if today is the start date of sub
        try:
            # Format inbound 2020-03-10T09:30:25
            start_date_datetime = datetime.strptime(
                start_date, "%Y-%m-%dT%H:%M:%S"
            )  
        except:
            # Format inbound 2020-03-10T09:30:25.812Z
            start_date_datetime = datetime.strptime(
                start_date, "%Y-%m-%dT%H:%M:%S.%fZ"
            )  

        if start_date_datetime.date() <= datetime.today().date():
            sender = SubscriptionNotificationEmailSender(
                post_data, "subscription_started"
            )
            sender.send()
            post_data["status"] = "In Progress"
            logger.info("Subscription Notification email sent")
        else:
            post_data["status"] = "Queued"

        post_data["end_date"] = end_date_str
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
        resp = stop_subscription(subscription)

        # Return updated subscriptions
        serializer = SubscriptionPatchResponseSerializer(resp)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class SubscriptionRestartView(APIView):
    """
    This is the SubscriptionRestartView APIView.
    This handles the API to restart a Subscription 
    """

    @swagger_auto_schema(
        request_body=SubscriptionPostSerializer,
        responses={"202": SubscriptionPatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Restart Subscription",
        operation_description="Endpoint for manually restart a subscription",
    )      
    def post(self, request, format=None):
        """Post method."""
        post_data = request.data.copy()
        sub_manager = SubscriptionCreationManager()
        created_response  = sub_manager.restart(post_data)
        
        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
