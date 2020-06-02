from api.serializers.subscriptions_serializers import (
    SubscriptionTargetSerializer,
    SubscriptionClicksSerializer,
    GoPhishResultSerializer,
    GoPhishGroupSerializer,
    GoPhishTimelineSerializer,
    GoPhishCampaignsSerializer,
    SubscriptionGetSerializer,
    SubscriptionPostSerializer,
    SubscriptionPostResponseSerializer,
    SubscriptionPatchSerializer,
    SubscriptionPatchResponseSerializer,
    SubscriptionDeleteResponseSerializer
)
from api.serializers.customer_serializers import CustomerContactSerializer
from datetime import datetime
from uuid import uuid4
import pytest

class TestSubscriptionTargetSerializer:
    
    def create(self, first_name, last_name, position, email):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'email': email
        }
        serializer = SubscriptionTargetSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create('firstname', 'lastname', 'someposition', 'fakeemail@domain.com')
        assert isinstance(serializer, SubscriptionTargetSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_fields_over_max_length(self):
        # first name, last name, and position fields should return an invalid serializer if they are over the max character length
        serializer = self.create('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
                                    'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll',
                                    'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp', 'email@domain.com')
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 3
        assert serializer.errors.get('first_name') is not None
        assert serializer.errors.get('last_name') is not None
        assert serializer.errors.get('position') is not None

class TestSubscriptionClicksSerializer:
    
    def create(self, source_ip, timestamp, target_uuid):
        data = {
            'source_ip': source_ip,
            'timestamp': timestamp,
            'target_uuid': target_uuid
        }
        serializer = SubscriptionClicksSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create('1.1.1.1', datetime.now(), uuid4())
        assert isinstance(serializer, SubscriptionClicksSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_source_ip_field_over_max_length(self):
        # source ip field should return an invalid serializer if it is over the max character limit
        serializer = self.create('1.1.54324.1231321.52432432.53253241341.5435.6.7.868768.4546.345435435.234.234.5234.22.344.1.2.3.4.5.6.7.8.8.6.54.24324.12.321.321.321',
                                    datetime.now(), uuid4())
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('source_ip') is not None

class TestGoPhishResultSerializer:
    
    def create(self, id, first_name, last_name, position, status, ip, latitude, longitude, send_date, reported):
        data = {
            'id': id,
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'status': status,
            'ip': ip,
            'latitude': latitude,
            'longitude': longitude,
            'send_date': send_date,
            'reported': reported
        }
        serializer = GoPhishResultSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(1, 'firstname', 'lastname', 'position', 'active', '1.1.1.1', 38.9432, -77.8951, datetime.now(), True)
        assert isinstance(serializer, GoPhishResultSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_fields_over_max_length(self):
        # first name, last name, and status fields should return an invalid serializer if thet are over the max character limit
        serializer = self.create(1, 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
                                'lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll', 'postion',
                                'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss', '1.1.1.1',
                                38.9432, -77.8951, datetime.now(), True)
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 3
        assert serializer.errors.get('first_name') is not None
        assert serializer.errors.get('last_name') is not None
        assert serializer.errors.get('status') is not None
    
    def test_serializer_missing_send_date_field(self):
        # missing send date field should return a valid serializer
        data = {
            'id': 1,
            'first_name': 'firstname',
            'last_name': 'lastname',
            'position': 'position',
            'status': 'status',
            'ip': '1.1.1.1',
            'latitude': -77.8951,
            'longitude': 38.9432,
            'reported': True
        }
        serializer = GoPhishResultSerializer(data=data)

        assert serializer.is_valid() is True
        assert len(serializer.errors) == 0
        assert serializer.errors.get('send_date') is None

class TestGoPhishGroupSerializer:

    def create(self, id, name, targets, modified_date):
        data = {
            'id': id,
            'name': name,
            'targets': targets,
            'modified_date': modified_date
        }
        serializer = GoPhishGroupSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(1, 'name', [], datetime.now())

        assert isinstance(serializer, GoPhishGroupSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_missing_id_field(self):
        # missing id field should return a valid serializer since it is not required
        data = {
            'name': 'name',
            'targets': [],
            'modified_date': datetime.now()
        }
        serializer = GoPhishGroupSerializer(data=data)

        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('id') is None

    def test_serializer_name_field_over_max_length(self):
        # name field over max character length should return an invalid serializer
        serializer = self.create(1, 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
                                [], datetime.now())

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('name') is not None

class TestGoPhishTimelineSerializer:

    def create(self, email, time, message, details):
        data = {
            'email': email,
            'time': time,
            'message': message,
            'details': details
        }
        serializer = GoPhishTimelineSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create('email@domain.com', datetime.now(), 'message', 'details')

        assert isinstance(serializer, GoPhishTimelineSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_missing_email_field(self):
        # missing email field should return a valid serializer
        data = {
            'time': datetime.now(),
            'message': 'message',
            'details': 'details'
        }
        serializer = GoPhishTimelineSerializer(data=data)

        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('email') is None
    
    def test_serializer_message_field_over_max_length(self):
        # message field over max character length should return an invalid serializer
        serializer = self.create('email@domain.com', datetime.now(), 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
                                'details')
        
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('message') is not None

class TestGoPhishCampaignsSerializer:
    
    def create(self, campaign_id, name, created_date, launch_date, send_by_date, completed_date, email_template, landing_page_template,
                status, results, groups, timeline, target_email_list):
        data = {
            'campaign_id': campaign_id,
            'name': name,
            'created_date': created_date,
            'launch_date': launch_date,
            'send_by_date': send_by_date,
            'completed_date': completed_date,
            'email_template': email_template,
            'landing_page_template': landing_page_template,
            'status': status,
            'results': results,
            'groups': groups,
            'timeline': timeline,
            'target_email_list': target_email_list
        }
        serializer = GoPhishCampaignsSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(1, 'name', datetime.now(), datetime.now(), datetime.now(), datetime.now(), 'emailtemplate', 
                                'landingpagetmeplate', 'active', [], [], [], [])
        
        assert isinstance(serializer, GoPhishCampaignsSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_fields_over_max_length(self):
        # name and status fields over character max length should return an invalid serializer
        serializer = self.create(1, 'nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                datetime.now(), datetime.now(), datetime.now(), datetime.now(), 'emailtemplate', 
                                'landingpagetmeplate', 'activeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                [], [], [], [])

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 2
        assert serializer.errors.get('name') is not None
        assert serializer.errors.get('status') is not None

    def test_serializer_missing_fields(self):
        # missing campaign id, send by date, completed date, email template, and etc. fields should return a valid serializer since they are not required
        data = {
            'name': 'name',
            'created_date': datetime.now(),
            'launch_date': datetime.now(),
            'status': 'actice',
            'results': [],
            'groups': [],
            'timeline': [],
        }
        serializer = GoPhishCampaignsSerializer(data=data)

        assert serializer.is_valid()
        assert len(serializer.errors) == 0

class TestSubscriptionGetSerializer:
    
    def create(self, subscription_uuid, customer_uuid, name, url, keywords, start_date, gophish_campaign_list, primary_contact,
                status, target_email_list, templates_selected_uuid_list, active, archived, manually_stopped, created_by, cb_timestamp,
                last_updated_by, lub_timestamp):
        
        data_subcritpion = {
            'subscription_uuid': subscription_uuid,
            'customer_uuid': customer_uuid,
            'name': name,
            'url': url,
            'keywords': keywords,
            'start_date': start_date,
            'gophish_campaign_list': gophish_campaign_list,
            'primary_contact': primary_contact,
            'status': status,
            'target_email_list': target_email_list,
            'templates_selected_uuid_list': templates_selected_uuid_list,
            'active': active,
            'archived': archived,
            'manually_stopped': manually_stopped,
            'created_by': created_by,
            'cb_timestamp': cb_timestamp,
            'last_updated_by': last_updated_by,
            'lub_timestamp': lub_timestamp
        }
        serializer = SubscriptionGetSerializer(data=data_subcritpion)
        return serializer

    def test_creation(self):
        data_customer = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
                'first_name': 'firstname',
                'last_name': 'last_name',
                'email': 'someemail@domain.com',
                'position': 'someposition'
        }
        serializer = self.create(uuid4(), uuid4(), 'name', 'https://www.someurl.com', 'keywords', datetime.now(), [], data_customer, 'status', [target_email_list_data],
                                [], True, False, False, 'createdby', datetime.now(), 'updatedby', datetime.now())

        assert isinstance(serializer, SubscriptionGetSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0
    
    def test_serializer_missing_fields(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
                'first_name': 'firstname',
                'last_name': 'last_name',
                'email': 'someemail@domain.com',
                'position': 'someposition'
        }
        data_subcritpion = {
            'subscription_uuid': uuid4(),
            'customer_uuid': uuid4(),
            # missing url and name fields should return an invalid serializer
            'keywords': 'keywords',
            'start_date': datetime.now(),
            'gophish_campaign_list': [],
            'primary_contact': customer_data,
            'status': 'status',
            'target_email_list': [target_email_list_data],
            'templates_selected_uuid_list': [],
            'active': True,
            'archived': False,
            'manually_stopped': False,
            'created_by': 'createdby',
            'cb_timestamp': datetime.now(),
            'last_updated_by': 'lastupdatedby',
            'lub_timestamp': datetime.now()
        }
        serializer = SubscriptionGetSerializer(data=data_subcritpion)

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 2
        assert serializer.errors.get('name') is not None
        assert serializer.errors.get('url') is not None
        

class TestSubscriptionPostSerializer:
    
    def create(self, customer_uuid, name, url, keywords, start_date, gophish_campaign_list, primary_contact, status, target_email_list,
                templates_selected_uuid_list, active, archived, manually_stopped):
        data = {
            'customer_uuid': customer_uuid,
            'name': name,
            'url': url,
            'keywords': keywords,
            'start_date': start_date,
            'gophish_campaign_list': gophish_campaign_list,
            'primary_contact': primary_contact,
            'status': status,
            'target_email_list': target_email_list,
            'templates_selected_uuid_list': templates_selected_uuid_list,
            'active': active,
            'archived': archived,
            'manually_stopped': manually_stopped
        }
        serializer = SubscriptionPostSerializer(data=data)
        return serializer

    def test_creation(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        serializer = self.create(uuid4(), 'name', 'www.someurl.com', 'keywords', datetime.now(), [], customer_data, 'status', [],
                                [], False, False, False)
        assert isinstance(serializer, SubscriptionPostSerializer)
        serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_missing_fields(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }

        data = {
            'customer_uuid': uuid4(),
            # missing name and url fields should return an invalid serializer
            'keywords': 'keywords',
            'start_date': datetime.now(),
            'gophish_campaign_list': [],
            'primary_contact': customer_data,
            'status': 'status',
            'target_email_list': [],
            'templates_selected_uuid_list': [],
            'active': True,
            'archived': False,
            'manually_stopped': False
        }
        serializer = SubscriptionPostSerializer(data=data)

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 2
        assert serializer.errors.get('name') is not None
        assert serializer.errors.get('url') is not None

class TestSubscriptionPostResponseSerializer:
    
    def create(self, subscription_uuid):
        data = {
            'subscription_uuid': subscription_uuid
        }
        serializer = SubscriptionPostResponseSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(uuid4())
        assert isinstance(serializer, SubscriptionPostResponseSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

class TestSubscriptionPatchSerializer:
    
    def create(self, customer_uuid, name, url, keywords, start_date, gophish_campaign_list, primary_contact,
                status, target_email_list, templates_selected_uuid_list, active, archived, manually_stopped):
        data = {
            'customer_uuid': customer_uuid,
            'name': name,
            'url': url,
            'keywords': keywords,
            'start_date': start_date,
            'gophish_campaign_list': gophish_campaign_list,
            'primary_contact': primary_contact,
            'status': status,
            'target_email_list': target_email_list,
            'templates_selected_uuid_list': templates_selected_uuid_list,
            'active': active,
            'archived': archived,
            'manually_stopped': manually_stopped
        }
        serializer = SubscriptionPatchSerializer(data=data)
        return serializer

    def test_creation(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
            'first_name': 'firstname',
            'last_name': 'last_name',
            'email': 'someemail@domain.com',
            'position': 'someposition'
        }
        serializer = self.create(uuid4(), 'name', 'https://www.someurl.com', 'keywords', datetime.now(), [], customer_data, 'status', [target_email_list_data], [], True, False, False)
        assert isinstance(serializer, SubscriptionPatchSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

    def test_serializer_missing_fields(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
            'first_name': 'firstname',
            'last_name': 'last_name',
            'email': 'someemail@domain.com',
            'position': 'someposition'
        }
        data = {
            'customer_uuid': uuid4(),
            # missing name and url fields should return a valid serializer
            'keywords': 'keywords',
            'start_date': datetime.now(),
            'gophish_campaign_list': [],
            'primary_contact': customer_data,
            'status': 'status',
            'target_email_list': [target_email_list_data],
            'templates_selected_uuid_list': [],
            'active': True,
            'archived': False,
            'manually_stopped': False
        }
        serializer = SubscriptionPatchSerializer(data=data)
        assert serializer.is_valid() 
        assert len(serializer.errors) == 0
        assert serializer.errors.get('name') is None
        assert serializer.errors.get('url') is None

class TestSubscriptionPatchResponseSerializer:
    
    def create(self, customer_uuid, name, url, keywords, start_date, gophish_campaign_list, primary_contact,
                status, target_email_list, templates_selected_uuid_list, active, archived, manually_stopped,
                created_by, cb_timestamp, last_updated_by, lub_timestamp):
        data = {
            'customer_uuid': customer_uuid,
            'name': name,
            'url': url,
            'keywords': keywords,
            'start_date': start_date,
            'gophish_campaign_list': gophish_campaign_list,
            'primary_contact': primary_contact,
            'status': status,
            'target_email_list': target_email_list,
            'templates_selected_uuid_list': templates_selected_uuid_list,
            'active': active,
            'archived': archived,
            'manually_stopped': manually_stopped,
            'created_by': created_by,
            'cb_timestamp': cb_timestamp,
            'last_updated_by': last_updated_by,
            'lub_timestamp': lub_timestamp
        }
        serializer = SubscriptionPatchResponseSerializer(data=data)
        return serializer

    def test_creation(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
            'first_name': 'firstname',
            'last_name': 'last_name',
            'email': 'someemail@domain.com',
            'position': 'someposition'
        }
        serializer = self.create(uuid4(), 'name', 'https://someurl.com', 'keywords', datetime.now(), [], customer_data, 'status', [target_email_list_data],
                                [], True, False, False, 'createdby', datetime.now(), 'lastupdatedby', datetime.now())
        assert isinstance(serializer, SubscriptionPatchResponseSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0
    
    def test_serializer_missing_fields(self):
        customer_data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'sometitle',
            'office_phone': '(208)453-9032',
            'mobile_phone': '(208)453-9032',
            'email': 'someemail@domain.com',
            'notes': 'somenotes',
            'active': True
        }
        target_email_list_data = {
            'first_name': 'firstname',
            'last_name': 'last_name',
            'email': 'someemail@domain.com',
            'position': 'someposition'
        }
        data = {
            'customer_uuid': uuid4(),
            # missing name field should return an invalid serializer
            'url': 'https://someurl.com',
            'keywords': 'keywords',
            'start_date': datetime.now(),
            'gophish_campaign_list': [],
            'primary_contact': customer_data,
            'status': 'status',
            'target_email_list': [target_email_list_data],
            # missing templates_selected_uuid_list fields should not result in an error
            'active': True,
            'archived': False,
            'manually_stopped': False,
            'created_by': 'createdby',
            'cb_timestamp': datetime.now(),
            'last_updated_by': 'lastupdatedby',
            'lub_timestamp': datetime.now()
        }
        serializer = SubscriptionPatchResponseSerializer(data=data)
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('name') is not None
        assert serializer.errors.get('templates_selected_uuid_list') is None
        

class TestSubscriptionDeleteResponseSerializer:
    
    def create(self, subscription_uuid):
        data ={
            'subscription_uuid': subscription_uuid
        }
        serializer = SubscriptionDeleteResponseSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(uuid4())
        assert isinstance(serializer, SubscriptionDeleteResponseSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0