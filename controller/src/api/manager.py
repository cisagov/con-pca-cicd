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
            self.generate_email_template(kwargs.get("name"), kwargs.get("template"))
        elif method == "landing_page":
            self.generate_landing_page(kwargs.get("name"), kwargs.get("template"))
        elif method == "user_group":
            self.generate_user_group()
        elif method == "sending_profile":
            self.generate_sending_profile()
        elif method == "campaign":
            self.generate_campaign()

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
    def generate_campaign(self):
        smtp = SMTP(name="HyreGuard")
        group = [Group(name="Email Group 1")]
        landing_page = Page(name="Name")
        email_template = Template(name="Name")

        campaign = Campaign(
            name="Test Campaign",
            groups=group,
            page=landing_page,
            template=email_template,
            smtp=smtp,
        )

        campaign = self.gp_api.campaigns.post(campaign)

        print("success")

    def generate_sending_profile(self):
        smtp = SMTP(name="HyreGuard")
        return self.gp_api.smtp.post(smtp=smtp)

    def generate_email_template(self, name: str, template: str):
        email_template = Template(name=name, html=template)
        return self.gp_api.templates.post(email_template)

    def generate_landing_page(self, name: str, template: str):
        landing_page = Page(name=name, html=template)
        return self.gp_api.pages.post(landing_page)

    def generate_user_group(self, num_groups=3, num_members=100):
        print("Creating new email groups...")
        group_names = []
        for group_index in range(0, num_groups):
            targets = []
            for target_index in range(0, num_members):
                first_name = faker.first_name()
                last_name = faker.last_name()
                email = "{}.{}@example.com".format(first_name, last_name)
                targets.append(
                    User(first_name=first_name, last_name=last_name, email=email)
                )
            group = Group(
                name="Email Group {}".format(group_index + 1), targets=targets
            )
            try:
                group = self.gp_api.groups.post(group)
            except Exception as e:
                print("Unable to post group: {}".format(e))
                break
            group_names.append(group.name)
        return group_names

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
