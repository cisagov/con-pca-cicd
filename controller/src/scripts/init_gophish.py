import os
import logging

# Third Party Libraries
from gophish import Gophish
from gophish.models import SMTP, Page


API_KEY = os.environ.get("GP_API_KEY")
URL = os.environ.get("GP_URL")
API = Gophish(API_KEY, host=URL, verify=False)

SENDING_PROFILES = [
    {
        "name": "SMTP",
        "host": os.environ.get("GP_SMTP_HOST"),
        "from_address": os.environ.get("GP_SMTP_FROM"),
        "username": os.environ.get("GP_SMTP_USER"),
        "password": os.environ.get("GP_SMTP_PASS"),
    },
]

LANDING_PAGES = [
    {
        "name": "Phished",
        "html": """
        <html>
            <head>
            <title>You've been phished!</title>
            </head>
            <body>
            <h1>You've Been Phished!</h1>
            <p>This is a message from a Gophish campaign</p>
            </body>
        </html>
        """,
    },
]


def create_sending_profile(profiles):
    """
    Create Gophish sending profiles
    """
    existing_names = {smtp.name for smtp in API.smtp.get()}

    for profile in profiles:
        profile_name = profile.get("name")
        if profile_name in existing_names:
            print(f"Sending profile, {profile_name}, already exists.. Skipping")
            continue
        smtp = SMTP(name=profile_name)
        smtp.host = profile.get("host")
        smtp.from_address = profile.get("from_address")
        smtp.username = profile.get("username")
        smtp.password = profile.get("password")
        smtp.interface_type = "SMTP"
        smtp.ignore_cert_errors = True
        smtp = API.smtp.post(smtp)
        print(f"Sending profile with id: {smtp.id} has been created")


def create_landing_page(pages):
    """
    Create a Gophish landing page
    """
    existing_names = {smtp.name for smtp in API.pages.get()}
    for page in pages:
        page_name = page.get("name")
        if page_name in existing_names:
            print(f"Landing page, {page_name}, already exists.. Skipping")
            continue
        landing_page = Page(name=page_name, html=page.get("html"))
        landing_page = API.pages.post(landing_page)
        print(f"Landing page with id: {landing_page.id} has been created")


def main():
    print("Step 1/2: Creating Sending Profiles")
    create_sending_profile(SENDING_PROFILES)
    print("Step 2/2: Creating Landing Pages")
    create_landing_page(LANDING_PAGES)
    return 0


if __name__ == "__main__":
    main()
