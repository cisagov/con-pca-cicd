from typing import Dict, List

from gophish import Gophish
from gophish.models import Campaign, Group, Page, SMTP, Template, User, Stat
from faker import Faker

from django.conf import settings


faker = Faker()


class CampaignManager:
    """
    GoPhish API Manager. TODO: create put and delete methods
    """

    def __init__(self):
        self.gp_api = Gophish(settings.GP_API_KEY, host=settings.GP_URL, verify=True)

    def create(self, method, **kwargs):
        if method == "email_template":
            return self.generate_email_template(
                kwargs.get("name"), kwargs.get("template")
            )
        elif method == "landing_page":
            return self.generate_landing_page(
                kwargs.get("name"), kwargs.get("template")
            )
        elif method == "user_group":
            return self.generate_user_group(
                kwargs.get("group_name"), kwargs.get("target_list")
            )
        elif method == "sending_profile":
            return self.generate_sending_profile()
        elif method == "campaign":
            return self.generate_campaign(
                kwargs.get("campaign_name"),
                kwargs.get("user_group"),
                kwargs.get("email_template"),
            )

    def get(self, method, **kwargs):
        if method == "email_template":
            return self.get_email_template(kwargs.get("template_id", None))
        elif method == "landing_page":
            return self.get_landing_page(kwargs.get("page_id", None))
        elif method == "user_group":
            return self.get_user_group(kwargs.get("group_id", None))
        elif method == "sending_profile":
            return self.get_sending_profile(kwargs.get("smtp_id", None))
        elif method == "campaign":
            return self.get_campaign(kwargs.get("campaign_id", None))
        else:
            return "method not found"

    # Create methods
    def generate_campaign(
        self, campaign_name: str = None, user_group=None, email_template=None
    ):
        smtp = SMTP(name="HyreGuard")
        landing_page = Page(name="Landing Page")

        campaign = Campaign(
            name=campaign_name,
            groups=[user_group],
            page=landing_page,
            template=email_template,
            smtp=smtp,
        )

        campaign = self.gp_api.campaigns.post(campaign)

        return campaign

    def generate_sending_profile(self):
        smtp = SMTP(name="HyreGuard")
        return self.gp_api.smtp.post(smtp=smtp)

    def generate_email_template(self, name: str, template: str):
        email_template = Template(name=name, html=template)
        return self.gp_api.templates.post(email_template)

    def generate_landing_page(self, name: str, template: str):
        landing_page = Page(name=name, html=template)
        return self.gp_api.pages.post(landing_page)

    def generate_user_group(self, group_name: str = None, target_list: Dict = None):
        users = [
            User(
                first_name=target.get("first_name"),
                last_name=target.get("last_name"),
                email=target.get("email"),
                position=target.get("position"),
            )
            for target in target_list
        ]

        target_group = Group(name=group_name, targets=users)
        group = self.gp_api.groups.post(target_group)
        return target_group

    # Get methods
    def get_campaign(self, campaign_id: int = None):
        if campaign_id:
            campaign = self.gp_api.campaigns.get(campaign_id=campaign_id)
        else:
            campaign = self.gp_api.campaigns.get()
        return campaign

    def get_sending_profile(self, smtp_id: int = None):
        if smtp_id:
            sending_profile = self.gp_api.smtp.get(smtp_id=smtp_id)
        else:
            sending_profile = self.gp_api.smtp.get()
        return sending_profile

    def get_email_template(self, template_id: int = None):
        if template_id:
            template = self.gp_api.templates.get(template_id=template_id)
        else:
            template = self.gp_api.templates.get()
        return template

    def get_landing_page(self, page_id: int = None):
        if page_id:
            landing_page = self.gp_api.pages.get(page_id=page_id)
        else:
            landing_page = self.gp_api.pages.get()
        return landing_page

    def get_user_group(self, group_id: int = None):
        if group_id:
            user_group = self.gp_api.groups.get(group_id=group_id)
        else:
            user_group = self.gp_api.groups.get()
        return user_group
