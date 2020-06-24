"""Subscription Utils file for api."""
# Standard Python Libraries
from datetime import datetime, timedelta
import logging

# Third-Party Libraries
from lcgit import lcg
from django.conf import settings
from celery.task.control import revoke


# Local Libraries
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
from api.serializers.subscriptions_serializers import SubscriptionPatchSerializer
from api.utils import db_utils as db
from api.utils import template_utils
from notifications.views import SubscriptionNotificationEmailSender
from tasks.tasks import email_subscription_report

logger = logging.getLogger()
campaign_manager = CampaignManager()
template_manager = TemplateManager()


def start_subscription(data=None, subscription_uuid=None):
    """Starts a new subscription."""
    if subscription_uuid:
        subscription = db.get_single(
            subscription_uuid, "subscription", SubscriptionModel, validate_subscription
        )
    else:
        subscription = data

    customer = __get_customer(subscription)

    if not subscription_uuid:
        subscription["name"] = __get_subscription_name(subscription, customer)
    start_date, end_date = __get_subscription_start_end_date(subscription)

    # Get batched personalized templates
    relevant_templates, personalized_templates = __personalize_template_batch(
        customer, subscription.get("url"), subscription.get("keywords"), subscription,
    )

    # Get batched targets
    batched_targets = __batch_targets(subscription)

    # Get all Landing pages or default
    # This is currently selecting the default page on creation.
    # landing_template_list = get_list({"template_type": "Landing"}, "template", TemplateModel, validate_template)
    landing_page = "Phished"

    gophish_campaigns = __process_batches(
        subscription,
        personalized_templates,
        batched_targets,
        landing_page,
        start_date,
        end_date,
    )

    subscription["gophish_campaign_list"] = gophish_campaigns
    subscription["templates_selected_uuid_list"] = relevant_templates
    subscription["end_date"] = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    subscription["status"] = __get_subscription_status(start_date)
    subscription["cycles"] = __get_subscription_cycles(
        gophish_campaigns, start_date, end_date
    )

    __send_start_notification(subscription, start_date)

    if subscription_uuid:
        db_data = {
            "gophish_campaign_list": gophish_campaigns,
            "templates_selected_uuid_list": relevant_templates,
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": __get_subscription_status(start_date),
            "cycles": __get_subscription_cycles(
                gophish_campaigns, start_date, end_date
            ),
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
    __create_scheduled_email_tasks(response)

    return response


def __get_subscription_name(post_data, customer):
    subscription_list = db.get_list(
        {"customer_uuid": customer["customer_uuid"]},
        "subscription",
        SubscriptionModel,
        validate_subscription,
    )

    if not subscription_list:
        base_name = f"{customer['identifier']}_1.1"
    else:
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

    return base_name


def __get_subscription_start_end_date(post_data):
    """Gets the start and end date for a subscription."""
    # split date string in case float is put at the end.
    date = post_data.get("start_date")
    now = datetime.now()

    if not date:
        date = now.strftime("%Y-%m-%dT%H:%M:%S")

    if not isinstance(date, datetime):
        start_date = datetime.strptime(date.split(".")[0], "%Y-%m-%dT%H:%M:%S")

        if start_date < now:
            start_date = now
    else:
        start_date = now

    end_date = start_date + timedelta(days=90)

    return start_date, end_date


def __get_customer(post_data):
    return db.get_single(
        post_data["customer_uuid"], "customer", CustomerModel, validate_customer
    )


def __get_email_templates():
    """Queries the database for all non-retired email templates."""
    return db.get_list(
        {"template_type": "Email", "retired": False},
        "template",
        TemplateModel,
        validate_template,
    )


def __get_relevant_templates(url, keywords, templates):
    """Returns 15 relevant templates."""
    template_data = {
        t.get("template_uuid"): t.get("descriptive_words") for t in templates
    }

    return (
        template_manager.get_templates(url, keywords, template_data)[:15]
        # if keywords
        # else []
    )


def __batch_templates(templates):
    """Batches templates into 3 groups of 5."""
    return [templates[x : x + 5] for x in range(0, len(templates), 5)]


def __batch_targets(post_data):
    targets = __lcgit_list_randomizer(post_data.get("target_email_list"))
    avg = len(targets) / float(3)

    return_lists = []
    last = 0.0
    while last < len(targets):
        return_lists.append(targets[int(last) : int(last + avg)])
        last += avg

    return return_lists


def __lcgit_list_randomizer(object_list):
    """
    Lcgit List Randomizer.

    This uses lcgit from https://github.com/cisagov/lcgit
    to genrate a random list order
    """
    random_list = []
    for item in lcg(object_list):
        random_list.append(item)
    return random_list


def __get_tags():
    """Returns a list of tags."""
    return db.get_list(None, "tag_definition", TagModel, validate_tag)


def __personalize_template_batch(customer, url, keywords, data):
    """Returns templates with tags replaced."""
    # Get tags for personalizing templates
    tags = __get_tags()

    # Gets list of all templates
    templates = __get_email_templates()

    # Finds relevant templates
    relevant_templates = __get_relevant_templates(url, keywords, templates)

    # Batch templates
    batched_templates = __batch_templates(relevant_templates)

    personalized_templates = []
    for batch in batched_templates:
        personalize_list = list(
            filter(lambda x: x["template_uuid"] in batch, templates)
        )

        personalized_data = template_utils.personalize_template(
            customer, personalize_list, data, tags
        )
        personalized_templates.append(personalized_data)

    return relevant_templates, personalized_templates


def __process_batches(
    post_data,
    personalized_templates,
    batched_targets,
    landing_page,
    start_date,
    end_date,
):
    send_by_date = start_date + timedelta(days=60)
    campaigns_info = [
        {
            "start_date": start_date,
            "send_by_date": send_by_date,
            "templates": [],
            "targets": [],
        },
        {
            "start_date": start_date,
            "send_by_date": send_by_date,
            "templates": [],
            "targets": [],
        },
        {
            "start_date": start_date,
            "send_by_date": send_by_date,
            "templates": [],
            "targets": [],
        },
    ]

    # Assign templates and targets
    for index, c in enumerate(campaigns_info):
        try:
            c["templates"] = personalized_templates[index]
        except Exception as e:
            logger.exception(e)
            pass
        try:
            c["targets"] = batched_targets[index]
        except Exception as e:
            logger.exception(e)
            pass

    # create campaigns
    group_number = 1
    gophish_campaigns = []
    existing_user_groups = [group.name for group in campaign_manager.get("user_group")]
    for campaign_info in campaigns_info:
        group_name = f"{post_data['name']}.Targets.{group_number}"
        campaign_info["name"] = f"{post_data['name']}.{group_number}"

        if group_name not in existing_user_groups:

            target_group = campaign_manager.create(
                "user_group",
                group_name=group_name,
                target_list=campaign_info["targets"],
            )

            campaign_info["deception_level"] = group_number
            gophish_campaigns.extend(
                __create_and_save_campaigns(
                    campaign_info, target_group, landing_page, end_date
                )
            )

        group_number += 1

    return gophish_campaigns


def __create_and_save_campaigns(campaign_info, target_group, landing_page, end_date):
    """
    Create and Save Campaigns.

    This method handles the creation of each campain with given template, target group, and data.
    """
    templates = campaign_info["templates"]
    targets = campaign_info["targets"]
    gophish_campaign_list = []
    # Create a GoPhish Campaigns
    for template in templates:
        # Create new template
        created_template = campaign_manager.generate_email_template(
            name=f"{campaign_info['name']}.{template['name']}",
            template=template["data"],
            subject=template["subject"],
        )
        campaign_start = campaign_info["start_date"].strftime("%Y-%m-%d")
        campaign_end = end_date.strftime("%Y-%m-%d")

        if created_template is not None:
            campaign_name = f"{campaign_info['name']}.{template['name']}.{campaign_start}.{campaign_end}"
            campaign = campaign_manager.create(
                "campaign",
                campaign_name=campaign_name,
                smtp_name="SMTP",
                # Replace with picked landing page, default init page now.
                page_name=landing_page,
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
                "created_date": template_utils.format_ztime(campaign.created_date),
                "launch_date": campaign_info["start_date"],
                "send_by_date": campaign_info["send_by_date"],
                "email_template": created_template.name,
                "email_template_id": created_template.id,
                "landing_page_template": campaign.page.name,
                "deception_level": campaign_info["deception_level"],
                "status": campaign.status,
                "results": [],
                "groups": [
                    campaign_serializers.CampaignGroupSerializer(target_group).data
                ],
                "timeline": [
                    {
                        "email": None,
                        "time": template_utils.format_ztime(campaign.created_date),
                        "message": "Campaign Created",
                        "details": "",
                    }
                ],
                "target_email_list": targets,
            }

            gophish_campaign_list.append(created_campaign)

    return gophish_campaign_list


def __send_start_notification(post_data, start_date):
    if start_date <= datetime.now():
        sender = SubscriptionNotificationEmailSender(post_data, "subscription_started")
        sender.send()


def __get_subscription_status(start_date):
    if start_date <= datetime.now():
        return "In Progress"
    else:
        return "Queued"


def __get_subscription_cycles(campaigns, start_date, end_date):
    campaigns_in_cycle = [c["campaign_id"] for c in campaigns]
    return [
        {
            "start_date": start_date,
            "end_date": end_date,
            "active": True,
            "campaigns_in_cycle": campaigns_in_cycle,
            "phish_results": {
                "sent": 0,
                "opened": 0,
                "clicked": 0,
                "submitted": 0,
                "reported": 0,
            },
        }
    ]


def __create_scheduled_email_tasks(created_response):
    if not settings.DEBUG:
        subscription_uuid = created_response.get("subscription_uuid")
        message_types = {
            "monthly_report": datetime.utcnow() + timedelta(days=30),
            "cycle_report": datetime.utcnow() + timedelta(days=90),
            "yearly_report": datetime.utcnow() + timedelta(days=365),
        }
        for message_type, send_date in message_types:
            try:
                task = email_subscription_report.apply_async(
                    args=[subscription_uuid, message_type], eta=send_date
                )
            except task.OperationalError as exc:
                logger.exception("Subscription task raised: %r", exc)


def stop_subscription(subscription):
    """
    Stops a given subscription.

    Returns updated subscription.
    """

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
