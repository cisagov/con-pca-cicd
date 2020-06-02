"""
Tests classes from models/subscription_models.py

Test 1. Define a new class, generate an object, assign values and assert if the object isinstance.
"""

from api.models.subscription_models import (
    SubscriptionTargetModel,
    SubscriptionClicksModel,
    SubscriptionModel,
    GoPhishResultModel,
    GoPhishGroupModel,
    GoPhishTimelineModel,
    GoPhishCampaignsModel,
)
from api.tests.models.test_customer_models import TestCustomerContactModel
import datetime
import uuid


class TestSubscriptionTargetModel:
    def create(
        self,
        first_name="Johnny",
        last_name="Bravo",
        position="CEO",
        email="johnny.bravo@test.com",
    ):
        subscription_target = SubscriptionTargetModel()
        subscription_target.first_name = first_name
        subscription_target.last_name = last_name
        subscription_target.position = position
        subscription_target.email = email

        return subscription_target

    # Test 1
    def test_creation(self):
        st = self.create()
        assert isinstance(st, SubscriptionTargetModel) is True


class TestSubscriptionClicksModel:
    def create(
        self,
        source_ip="111.111.11.11",
        timestamp=datetime.datetime.now(),
        target_uuid=uuid.uuid4(),
    ):
        subscription_clicks = SubscriptionClicksModel()
        subscription_clicks.source_ip = source_ip
        subscription_clicks.timestamp = timestamp
        subscription_clicks.target_uuid = target_uuid

        return subscription_clicks

    # Test 1
    def test_creation(self):
        sc = self.create()
        assert isinstance(sc, SubscriptionClicksModel) is True


class TestGoPhishResultModel:
    def create(
        self,
        first_name="Johny",
        last_name="Bravo",
        position="CEO",
        status="Active",
        ip="111.111.11.11",
        latitude=36.0544,
        longitude=112.1401,
        send_date=datetime.datetime.now(),
        reported=True,
    ):
        goPhish_result = GoPhishResultModel()
        goPhish_result.first_name = first_name
        goPhish_result.last_name = last_name
        goPhish_result.position = position
        goPhish_result.status = status
        goPhish_result.ip = ip
        goPhish_result.latitude = latitude
        goPhish_result.longitude = longitude
        goPhish_result.send_date = send_date
        goPhish_result.reported = reported

        return goPhish_result

    # Test 1
    def test_creation(self):
        gpr = self.create()
        assert isinstance(gpr, GoPhishResultModel) is True


class TestGoPhishGroupModel:
    test_subscription_target_model = TestSubscriptionTargetModel()

    def create(
        self,
        id=int(1),
        name="Test Group",
        targets=[
            test_subscription_target_model.create(),
            test_subscription_target_model.create(),
        ],
        modified_date=datetime.datetime.now(),
    ):
        goPhish_group = GoPhishGroupModel()
        goPhish_group.id = id
        goPhish_group.name = name
        goPhish_group.targets = targets
        goPhish_group.modified_date = modified_date

        return goPhish_group

    # Test 1
    def test_creation(self):
        gpg = self.create()
        assert isinstance(gpg, GoPhishGroupModel) is True


class TestGoPhishTimelineModel:
    def create(
        self,
        email="johndoe@test.com",
        time=datetime.datetime.now(),
        message="Test Message",
        details="{ name: 'John', age: 31, city: 'New York' }",
    ):
        goPhish_timeline = GoPhishTimelineModel()
        goPhish_timeline.email = email
        goPhish_timeline.time = time
        goPhish_timeline.message = message
        goPhish_timeline.details = details

        return goPhish_timeline

    # Test 1
    def test_creation(self):
        gpt = self.create()
        assert isinstance(gpt, GoPhishTimelineModel) is True


class TestGoPhishCampaignsModel:
    # Used to create test lists
    test_results = TestGoPhishResultModel()
    test_groups = TestGoPhishGroupModel()
    test_timeline = TestGoPhishTimelineModel()
    test_target_email_list = TestSubscriptionTargetModel()

    def create(
        self,
        campaign_id=int(1),
        name="Campaign Test",
        created_date=datetime.datetime.now(),
        launch_date=datetime.datetime.now(),
        send_by_date=datetime.datetime.now(),
        completed_date=datetime.datetime.now(),
        email_template="Template Name Here",
        landing_page_template="Landing Page Here",
        status="Active",
        results=[test_results.create(), test_results.create()],
        groups=[test_groups.create(), test_groups.create()],
        timeline=[test_timeline.create(), test_timeline.create()],
        target_email_list=[
            test_target_email_list.create(),
            test_target_email_list.create(),
        ],
    ):
        goPhish_campaigns = GoPhishCampaignsModel()
        goPhish_campaigns.campaign_id = campaign_id
        goPhish_campaigns.name = name
        goPhish_campaigns.created_date = created_date
        goPhish_campaigns.launch_date = launch_date
        goPhish_campaigns.completed_date = completed_date
        goPhish_campaigns.email_template = email_template
        goPhish_campaigns.landing_page_template = landing_page_template
        goPhish_campaigns.status = status
        goPhish_campaigns.results = results
        goPhish_campaigns.groups = groups
        goPhish_campaigns.timeline = timeline
        goPhish_campaigns.target_email_list = target_email_list

        return goPhish_campaigns

    # Test 1
    def test_creation(self):
        gpc = self.create()
        assert isinstance(gpc, GoPhishCampaignsModel) is True


class TestSubscriptionModel:
    test_gophish_campaign_list = TestGoPhishCampaignsModel()
    test_primary_contact = TestCustomerContactModel()
    test_target_email_list = TestSubscriptionTargetModel()

    def create(
        self,
        subscription_uuid=uuid.uuid4(),
        customer_uuid=uuid.uuid4(),
        name="Sub Test",
        url="www.google.com",
        keywords="Test, Yes, No",
        start_date=datetime.datetime.now(),
        gophish_campaign_list=[
            test_gophish_campaign_list.create(),
            test_gophish_campaign_list.create(),
        ],
        primary_contact=test_primary_contact.create(),
        status="Active",
        target_email_list=[
            test_target_email_list.create(),
            test_target_email_list.create(),
        ],
        templates_selected_uuid_list=["Test1", "Test2"],
        active=True,
        created_by="Johnny Bravo",
        cb_timestamp=datetime.datetime.now(),
        last_updated_by="Jimmy Bravo",
        lub_timestamp=datetime.datetime.now(),
    ):
        subscription_model = SubscriptionModel()
        subscription_model.subscription_uuid = subscription_uuid
        subscription_model.customer_uuid = customer_uuid
        subscription_model.name = name
        subscription_model.url = url
        subscription_model.keywords = keywords
        subscription_model.start_date = start_date
        subscription_model.gophish_campaign_list = gophish_campaign_list
        subscription_model.primary_contact = primary_contact
        subscription_model.status = status
        subscription_model.target_email_list = target_email_list
        subscription_model.templates_selected_uuid_list = templates_selected_uuid_list
        subscription_model.active = active
        subscription_model.created_by = created_by
        subscription_model.cb_timestamp = cb_timestamp
        subscription_model.last_updated_by = last_updated_by
        subscription_model.lub_timestamp = lub_timestamp

        return subscription_model

    # Test 1
    def test_creation(self):
        sm = self.create()
        assert isinstance(sm, SubscriptionModel) is True
