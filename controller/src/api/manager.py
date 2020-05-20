"""GoPhish API Manager."""

# Standard Python Libraries
import re
import logging
from typing import Dict

# Third-Party Libraries
import requests
from faker import Faker
from django.conf import settings
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

# GoPhish Libraries
from gophish import Gophish
from gophish.models import SMTP, Campaign, Group, Page, Template, User


logger = logging.getLogger(__name__)
faker = Faker()
vectorizer = TfidfVectorizer()


class TemplateManager:
    """Template calculator"""

    def __init__(self):
        pass

    def preprocess_keywords(self, url: str, keywords: str):
        """
        Extract text from the given url
        Concatenate a bag of keywords from user input
        clean text by converting words to lower case,
        removing punctuation and numbers
        """
        web_text = ""
        if url != None:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            headers = {"Content-Type": "text/html"}
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, "lxml")
            web_text = re.sub(r"[^A-Za-z]+", " ", soup.get_text().lower())

        if keywords == None:
            keywords = ""
            
        return web_text + keywords

    def get_templates(self, url: str, keywords: str, template_data):
        """
        Return highest relative templates using tf-idf and cosine similarity algorithms
        based on customer keywords
        """
        template_uuids = [*template_data.keys()]
        preprocessed_data = [self.preprocess_keywords(url, keywords)] + [
            *template_data.values()
        ]
        
        while("" in preprocessed_data) : 
            preprocessed_data.remove("") 

        if not preprocessed_data:
            return []

        docs_tfidf = vectorizer.fit_transform(preprocessed_data)
        cosine_similarities = cosine_similarity(docs_tfidf[:1], docs_tfidf).flatten()
        cosine_similarities = cosine_similarities[1:]

        context = [
            i
            for _, i in sorted(
                dict(zip(cosine_similarities, template_uuids)).items(), reverse=True
            )
        ]

        return context


class CampaignManager:
    """GoPhish API Manager. TODO: create put and delete methods."""

    def __init__(self):
        """Init."""
        self.gp_api = Gophish(settings.GP_API_KEY, host=settings.GP_URL, verify=True)

    def create(self, method, **kwargs):
        """Create Method."""
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
                kwargs.get("smtp_name"),
                kwargs.get("page_name"),
                kwargs.get("user_group"),
                kwargs.get("email_template"),
            )

    def get(self, method, **kwargs):
        """GET Method."""
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
        self,
        campaign_name: str,
        smtp_name: str,
        page_name: str,
        user_group=None,
        email_template=None,
    ):
        """Generate campaign Method."""
        smtp = SMTP(name=smtp_name)
        landing_page = Page(name=page_name)

        campaign = Campaign(
            name=campaign_name,
            groups=[user_group],
            page=landing_page,
            template=email_template,
            smtp=smtp,
            url=settings.PHISH_URL,
        )

        campaign = self.gp_api.campaigns.post(campaign)

        return campaign

    def generate_sending_profile(self):
        """Generate Sending Profiles."""
        smtp = SMTP(name="HyreGuard")
        return self.gp_api.smtp.post(smtp=smtp)

    def generate_email_template(self, name: str, template: str):
        """Generate Email Templates."""
        existing_names = {email.name for email in self.gp_api.templates.get()}
        if name in existing_names:
            logger.info("Template, {}, already exists.. skipping".format(name))
            return
        email_template = Template(name=name, html=template)
        return self.gp_api.templates.post(email_template)

    def generate_landing_page(self, name: str, template: str):
        """Generate Landing Page."""
        landing_page = Page(name=name, html=template)
        return self.gp_api.pages.post(landing_page)

    def generate_user_group(self, group_name: str = None, target_list: Dict = None):
        """Generate User Group."""
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
        self.gp_api.groups.post(target_group)
        return target_group

    # Get methods
    def get_campaign(self, campaign_id: int = None):
        """GET Campaign."""
        if campaign_id:
            campaign = self.gp_api.campaigns.get(campaign_id=campaign_id)
        else:
            campaign = self.gp_api.campaigns.get()
        return campaign

    def get_sending_profile(self, smtp_id: int = None):
        """GET Sending Profile."""
        if smtp_id:
            sending_profile = self.gp_api.smtp.get(smtp_id=smtp_id)
        else:
            sending_profile = self.gp_api.smtp.get()
        return sending_profile

    def get_email_template(self, template_id: int = None):
        """GET Email Temp."""
        if template_id:
            template = self.gp_api.templates.get(template_id=template_id)
        else:
            template = self.gp_api.templates.get()
        return template

    def get_landing_page(self, page_id: int = None):
        """GET landingpage."""
        if page_id:
            landing_page = self.gp_api.pages.get(page_id=page_id)
        else:
            landing_page = self.gp_api.pages.get()
        return landing_page

    def get_user_group(self, group_id: int = None):
        """GET User group."""
        if group_id:
            user_group = self.gp_api.groups.get(group_id=group_id)
        else:
            user_group = self.gp_api.groups.get()
        return user_group
