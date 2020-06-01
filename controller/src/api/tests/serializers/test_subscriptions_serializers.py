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
        serializer = self.create(1, 'nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                datetime.now(), datetime.now(), datetime.now(), datetime.now(), 'emailtemplate', 
                                'landingpagetmeplate', 'activeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                [], [], [], [])

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 2
        assert serializer.errors.get('name') is not None
        assert serializer.errors.get('status') is not None

    def test_serializer_missing_fields(self):
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
        
        data = {
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
        serializer = SubscriptionGetSerializer(data=data)
        return serializer

class TestSubscriptionPostSerializer:
    pass

class TestSubscriptionPostResponseSerializer:
    pass

class TestSubscriptionPatchSerializer:
    pass

class TestSubscriptionPatchResponseSerializer:
    pass

class TestSubscriptionDeleteResponseSerializer:
    pass