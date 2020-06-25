"""Subscription Campaigns."""

# Standard Python Libraries
from datetime import timedelta
import logging

# Third-Party Libraries
from api.manager import CampaignManager
from api.serializers import campaign_serializers
from api.utils.generic import format_ztime
from api.utils.subscription.targets import assign_targets

logger = logging.getLogger()

campaign_manager = CampaignManager()


def generate_campaigns(subscription, landing_page, sub_levels):
    """Generate_campaigns.

    Args:
        subscription (dict): subscription
        sub_level (dict): sub_level
        landing_page (dict): landing_page

    Returns:
        list(dict): gophish_campaigns
    """
    gophish_campaigns = []
    for k in sub_levels.keys():
        # Assign targets to templates in each group
        sub_levels[k] = assign_targets(sub_levels[k])
        gophish_campaigns.extend(
            create_campaign(subscription, sub_levels[k], landing_page)
        )

    return gophish_campaigns


def create_campaign(subscription, sub_level, landing_page):
    """Create campaign.

    Args:
        subscription (dict): subscription
        sub_level (dict): sub_level
        landing_page (dict): landing_page

    Returns:
        list(dict): gophish_campaigns
    """
    gophish_campaigns = []

    for index, k in enumerate(sub_level["template_targets"].keys()):
        group_name = (
            f"{subscription['name']}.Targets.{sub_level['deception_level']}.{index}"
        )

        target_group = campaign_manager.create(
            "user_group",
            group_name=group_name,
            target_list=sub_level["template_targets"][k],
        )

        template = list(
            filter(
                lambda x: x["template_uuid"] == k, sub_level["personalized_templates"]
            )
        )[0]

        gophish_campaigns.append(
            __create_campaign(
                subscription=subscription,
                target_group=target_group,
                landing_page=landing_page,
                template=template,
                targets=sub_level["template_targets"][k],
                start_date=sub_level["start_date"],
                deception_level=sub_level["deception_level"],
                index=index,
            )
        )

    return gophish_campaigns


def __create_campaign(
    subscription,
    target_group,
    landing_page,
    template,
    targets,
    start_date,
    deception_level,
    index,
):
    """
    Create and Save Campaigns.

    This method handles the creation of each campain with given template, target group, and data.
    """
    base_name = f"{subscription['name']}.{deception_level}.{index}"

    created_template = campaign_manager.generate_email_template(
        name=f"{base_name}.{template['name']}",
        template=template["data"],
        subject=template["subject"],
    )
    campaign_start = start_date
    campaign_end = start_date + timedelta(days=60)

    campaign_name = f"{base_name}.{template['name']}.{campaign_start.strftime('%Y-%m-%d')}.{campaign_end.strftime('%Y-%m-%d')}"

    sending_profile_name = subscription.get("sending_profile_name")

    campaign = campaign_manager.create(
        "campaign",
        campaign_name=campaign_name,
        smtp_name=sending_profile_name,
        page_name=landing_page,
        user_group=target_group,
        email_template=created_template,
        launch_date=start_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        send_by_date=(campaign_end).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    )

    logger.info("campaign created: {}".format(campaign))

    default_phish_results = {
        "sent": 0,
        "opened": 0,
        "clicked": 0,
        "submitted": 0,
        "reported": 0,
    }

    return {
        "campaign_id": campaign.id,
        "name": campaign_name,
        "created_date": format_ztime(campaign.created_date),
        "launch_date": campaign_start,
        "send_by_date": campaign_end,
        "email_template": created_template.name,
        "email_template_id": created_template.id,
        "template_uuid": template["template_uuid"],
        "landing_page_template": campaign.page.name,
        "deception_level": deception_level,
        "status": campaign.status,
        "results": [],
        "phish_results": default_phish_results,
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
