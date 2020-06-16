from io import StringIO
import json
from django.conf import settings

import sys, os

sys.path.insert(0, "/app")  # /home/projects/my-djproj
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from api.views.utils.subscription_utils import SubscriptionCreationManager

# this is the post data
# need to deserialize from jason to an object and pass to the restart method.

import ptvsd

ptvsd.enable_attach()
ptvsd.wait_for_attach()

print("break here")

io = StringIO(
    '{"active": true, "customer_uuid": "d59eb615-6f5f-4ed5-ba06-3634e75548fc", "dhs_primary_contact": {"active": true, "email": "Bigg.Daemon@inl.com", "first_name": "Bigg", "last_name": "Daemon", "mobile_phone": "555-555-5555", "office_phone": "555-555-5555"}, "gophish_campaign_list": [], "keywords": "research development government work job", "name": "changeme", "primary_contact": {"active": true, "email": "Matt.Daemon@example.com", "first_name": "Matt", "last_name": "Daemon", "mobile_phone": "555-555-5555", "office_phone": "555-555-5555"}, "start_date": "2020-06-13T01:12:45", "status": "  Waiting on SRF", "target_email_list": [{"email": "Bat.Man@example.com", "first_name": "Bat", "last_name": "Man", "position": "admin"}, {"email": "Ben.Aflex@example.com", "first_name": "Ben", "last_name": "Aflex", "position": "admin"}, {"email": "David.Young@example.com", "first_name": "David", "last_name": "Young", "position": "intern"}, {"email": "George.Clooney@example.com", "first_name": "George", "last_name": "Clooney", "position": "intern"}, {"email": "Jane.Doe@example.com", "first_name": "Jane", "last_name": "Doe", "position": "intern"}, {"email": "Jane.Moore@example.com", "first_name": "Jane", "last_name": "Moore", "position": "manager"}, {"email": "John.Smith@example.com", "first_name": "John", "last_name": "Smith", "position": "manager"}], "templates_selected_uuid_list": [], "url": "https://inl.gov"}'
)
post_data = json.load(io)
SubscriptionCreationManager.restart(post_data)
