from api.serializers.campaign_serializers import (
    CampaignResultSerializer,
    CampaignGroupTargetSerializer,
    CampaignGroupSerializer,
    CampaignEventSerializer,
    CampaignSerializer,
)
from datetime import datetime
from uuid import uuid4
import pytest

class TestCampaignResultSerializer:
    
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
        serilaizer = CampaignResultSerializer(data=data)
        return serilaizer

    def test_creation(self):
        serializer = self.create('12345', 'firstname', 'lastname', 'someposition', 'inactive', '1.1.1.1', 38.9432, -77.8951, '2020-03-29 10:26:23.473031', True)
        assert isinstance(serializer, CampaignResultSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('active') is None

    def test_serializer_missing_reported_field(self): 
        data = {
            'id': 12345,
            'first_name': 'firstname',
            'last_name': 'lastname',
            'position': 'someposition',
            'status': 'inactive',
            'ip': '1.1.1.1',
            'latitude': 38.9432,
            'longitude': -77.8951,
            'send_date': '2020-03-29 10:26:23.473031'
        }
        serializer = CampaignResultSerializer(data=data)

        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('reported') is None

    def test_serializer_missing_send_date_field(self): 
        data = {
            'id': 12345,
            'first_name': 'firstname',
            'last_name': 'lastname',
            'position': 'someposition',
            'status': 'inactive',
            'ip': '1.1.1.1',
            'latitude': 38.9432,
            'longitude': -77.8951,
            'reported': False
        }
        serializer = CampaignResultSerializer(data=data)

        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('send_date') is None

class TestCampaignGroupTargetSerializer:
    
    def create(self, email, first_name, last_name, position):
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'position': position
        }
        serializer = CampaignGroupTargetSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create('someemail@domain.com', 'firstname', 'lastname', 'someposition')
        assert isinstance(serializer, CampaignGroupTargetSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

class TestCampaignGroupSerializer:
    
    def create(self, id, name, targets, modified_date):
        data = {
            'id': id,
            'name': name,
            'targets': targets,
            'modified_date': modified_date,
        }
        serializer = CampaignGroupSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create(12943, 'somename', [], '2020-03-29 10:26:23.473031')
        assert isinstance(serializer, CampaignGroupSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0
        assert serializer.errors.get('name') is None

    def test_serializer_missing_name_field(self):
        data = {
            'id': id,
            'targets': [],
            'modified_date': '2020-03-29 10:26:23.473031'
        }
        serializer = CampaignGroupSerializer(data=data)

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('name') is not None

class TestCampaignEventSerializer:
    
    def create(self, email, time, message, details):
        data = {
            'email': email,
            'time': time,
            'message': message,
            'details': details
        }
        serializer = CampaignEventSerializer(data=data)
        return serializer

    def test_creation(self):
        serializer = self.create('someemail@domain.com', '2020-03-29 10:26:23.473031', 'some test message', 'some test details')
        assert isinstance(serializer, CampaignEventSerializer)
        assert serializer.is_valid()
        assert len(serializer.errors) == 0

class TestCampaignSerializer:
    
    def create(self, id, name, created_date, launch_date, send_by_date, completed_by_date, status, url, results, group, timeline):
        data = {
            'id': id,
            'name': name,
            'created_date': created_date,
            'launch_date': launch_date,
            'send_by_date': send_by_date,
            'completed_date': completed_by_date,
            'status': status,
            'url': url,
            'results': results,
            'groups': group,
            'timeline': timeline
        }
        serializer = CampaignSerializer(data = data)
        return serializer

    def test_creation(self):
        serializer = self.create(1234, 'somename', '2020-03-29 10:26:23.473031', '2020-04-29 10:26:23.473031', '2020-03-29 10:26:23.473031', '2020-03-29 10:26:23.473031', 'active', 'https://fakedomain.com', [],[],[])
        
        assert isinstance(serializer, CampaignSerializer)
        serializer.is_valid()
        print(serializer.errors)
        assert len(serializer.errors) == 0


    def test_serializer_missing_name_field(self):
        data = {
            'id': id,
            'created_date': '2020-03-29 10:26:23.473031',
            'launch_date': '2020-03-29 10:26:23.473031',
            'send_by_date': '2020-03-29 10:26:23.473031',
            'completed_date': '2020-03-29 10:26:23.473031',
            'status': 'active',
            'url': 'https://fakedomain.com',
            'results': [],
            'groups': [],
            'timeline': []
        }
        serializer = CampaignSerializer(data = data)

        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('name') is not None