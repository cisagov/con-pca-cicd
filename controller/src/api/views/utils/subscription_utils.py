"""
Subscription Manager

This should handle subscription creation, stop and restart
for the gophish campaigns.
"""
# Standard Python Libraries
from datetime import datetime
import logging

# Third-Party Libraries
# Local
from api.manager import CampaignManager, TemplateManager
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

logger = logging.getLogger(__name__)
# GoPhish API Manager
campaign_manager = CampaignManager()
# Template Calculator Manager
template_manager = TemplateManager()



class SubscriptionCreationManager:

    def start(self):
        raise NotImplementedError

    def restart(self, post_data, format=None):
        # get customer data
        customer = get_single(post_data["customer_uuid"], "customer", CustomerModel, validate_customer)

        # Get start date then quater of start date and create names to check
        start_date = post_data.get("start_date", datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        )
        #check to ensure the start date was not in the past
        today = datetime.now()
        if start_date < today:
            start_date = today


        end_date = get_sub_end_date(start_date)
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        # Get all Email templates for calc
        email_template_params = {"template_type": "Email", "retired": False}
        template_list = get_list(
            email_template_params, "template", TemplateModel, validate_template
        )

        # Get all Landing pages or default
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
        post_data["end_date"] = end_date_str
        created_response = save_single(
            post_data, "subscription", SubscriptionModel, validate_subscription
        )

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
