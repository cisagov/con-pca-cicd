from api.utils.subscription.subscriptions import (
    get_subscription,
    create_subscription_name,
    calculate_subscription_start_end_date,
    get_subscription_status,
    get_subscription_cycles,
    send_start_notification,
    create_scheduled_email_tasks,
)
from api.utils.subscription.template_selector import personalize_template_batch
from api.utils.subscription.targets import batch_targets
from api.utils.customer.customers import get_customer
from api.utils.subscription.campaigns import generate_campaigns
from api.utils import db_utils as db
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.serializers.subscriptions_serializers import SubscriptionPatchSerializer
from api.utils.template.templates import deception_level

from django.conf import settings

from celery.task.control import revoke

from api.manager import CampaignManager
from datetime import datetime

import logging


def start_subscription(data=None, subscription_uuid=None):
    """
    Returns a subscription from database

    Parameters:
        data (dict): posted data of subscription to start.
        subscription_uuid (str): uuid of subscription to restart.


    Returns:
        dict: returns response of updated/created subscription from database.
    """
    if subscription_uuid:
        subscription = get_subscription(subscription_uuid)
    else:
        subscription = data

    # calculate start and end date to subscription
    start_date, end_date = calculate_subscription_start_end_date(
        subscription.get("start_date")
    )

    # Get details for the customer that is attached to the subscription
    customer = get_customer(data["customer_uuid"])

    # Create the needed subscription levels to fill.
    sub_levels = {
        "high": {
            "start_date": start_date,
            "end_date": end_date,
            "template_targets": {},
            "template_uuids": [],
            "personalized_templates": [],
            "targets": [],
            "deception_level": deception_level.get("high"),
        },
        "moderate": {
            "start_date": start_date,
            "end_date": end_date,
            "template_targets": {},
            "template_uuids": [],
            "personalized_templates": [],
            "targets": [],
            "deception_level": deception_level.get("moderate"),
        },
        "low": {
            "start_date": start_date,
            "end_date": end_date,
            "template_targets": {},
            "template_uuids": [],
            "personalized_templates": [],
            "targets": [],
            "deception_level": deception_level.get("low"),
        },
    }

    # if a new subscription is being created, a name needs generated.
    if not subscription_uuid:
        subscription["name"] = create_subscription_name(customer)

    logging.info(f"subscription_name={subscription['name']}")

    # get personalized and selected template_uuids
    sub_levels = personalize_template_batch(customer, subscription, sub_levels)

    # get targets assigned to each group
    sub_levels = batch_targets(subscription, sub_levels)

    # Get all Landing pages or default
    # This is currently selecting the default page on creation.
    # landing_template_list = get_list({"template_type": "Landing"}, "template", TemplateModel, validate_template)
    landing_page = "Phished"

    subscription["gophish_campaign_list"] = generate_campaigns(
        subscription, landing_page, sub_levels
    )
    selected_templates = []
    for v in sub_levels.values():
        selected_templates.extend(list(v["template_targets"].keys()))
    subscription["templates_selected_uuid_list"] = selected_templates

    subscription["end_date"] = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    subscription["status"] = get_subscription_status(start_date)
    subscription["cycles"] = get_subscription_cycles(
        subscription["gophish_campaign_list"], start_date, end_date
    )

    if subscription_uuid:
        db_data = {
            "gophish_campaign_list": subscription["gophish_campaign_list"],
            "templates_selected_uuid_list": subscription[
                "templates_selected_uuid_list"
            ],
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": subscription["status"],
            "cycles": subscription["cycles"],
        }
        response = db.update_single(
            subscription_uuid,
            db_data,
            "subscription",
            SubscriptionModel,
            validate_subscription,
        )
    else:
        response = db.save_single(
            subscription, "subscription", SubscriptionModel, validate_subscription
        )

    # Schedule client side reports emails
    if settings.DEBUG:
        tasks = create_scheduled_email_tasks(response)
        subscription["tasks"] = tasks

    send_start_notification(subscription, start_date)

    return response


def stop_subscription(subscription):
    """
    Stops a given subscription.

    Returns updated subscription.
    """
    campaign_manager = CampaignManager()

    def stop_campaign(campaign):
        """
        Stops a given campaign.

        Returns updated Campaign
        """
        campaign_manager.complete_campaign(campaign_id=campaign["campaign_id"])
        campaign["status"] = "stopped"
        campaign["completed_date"] = datetime.now()
        return campaign

    # Stop Campaigns
    updated_campaigns = list(map(stop_campaign, subscription["gophish_campaign_list"]))

    # Remove subscription tasks from the scheduler
    if subscription["tasks"]:
        [revoke(task["task_uuid"], terminate=True) for task in subscription["tasks"]]

    # Update subscription
    subscription["gophish_campaign_list"] = updated_campaigns
    subscription["active"] = False
    subscription["manually_stopped"] = True
    subscription["active_task"] = False
    subscription["status"] = "stopped"
    resp = db.update_single(
        uuid=subscription["subscription_uuid"],
        put_data=SubscriptionPatchSerializer(subscription).data,
        collection="subscription",
        model=SubscriptionModel,
        validation_model=validate_subscription,
    )

    return resp
