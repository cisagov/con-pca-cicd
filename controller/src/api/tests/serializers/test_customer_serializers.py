from api.serializers.customer_serializers import (
    CustomerContactSerializer,
    CustomerGetSerializer,
    CustomerPostSerializer,
    CustomerPostResponseSerializer,
    CustomerPatchSerializer,
    CustomerPatchResponseSerializer,
    CustomerDeleteResponseSerializer
)

from api.models.customer_models import CustomerContactModel


from datetime import datetime
from uuid import uuid4
import json

class TestCustomerContactSerializer:
    def test_serializer(self):
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'title',
            'office_phone': '111-222-3333',
            'mobile_phone': '444-555-6666',
            'email': 'email@email.com',
            'notes': 'notes',
            'active': True
        }

        serializer = CustomerContactSerializer(data=data)
        assert serializer.is_valid() is True

    def test_serializer_null_active(self):
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'title': 'title',
            'office_phone': '111-222-3333',
            'mobile_phone': '444-555-6666',
            'email': 'email@email.com',
            'notes': 'notes',
            'active': None
        }

        serializer = CustomerContactSerializer(data=data)
        assert serializer.is_valid() is False
        assert len(serializer.errors) == 1
        assert serializer.errors.get('active') is not None


class TestCustomerGetSerializer:
    def create(self, customer_uuid=uuid4(), name='JimmyJohns', identifier='id', address_1='123 Street Street', address_2='456 Road Way', city='Citysburg', state='New Kansas', zip_code='12345', contact_list=[], created_by='Creator', cb_timestamp=datetime(1234, 5, 6), last_updated_by='Updater', lub_timestamp=datetime(9876, 5, 4)):
        customer_get = CustomerGetSerializer()
        customer_get.customer_uuid = customer_uuid
        customer_get.name = name
        customer_get.identifier = identifier
        customer_get.address_1 = address_1
        customer_get.address_2 = address_2
        customer_get.city = city
        customer_get.state = state
        customer_get.zip_code = zip_code
        customer_get.contact_list = contact_list
        customer_get.created_by = created_by
        customer_get.cb_timestamp = cb_timestamp
        customer_get.last_updated_by = last_updated_by
        customer_get.lub_timestamp = lub_timestamp
        return customer_get

    def test_creation(self):
        cg = self.create()
        assert isinstance(cg, CustomerGetSerializer) is True


class TestCustomerPostSerializer:
    def create(self, name='JimmyJohns', identifier='id', address_1='123 Street Street', address_2='456 Road Way', city='Citysburg', state='New Kansas', zip_code='12345', contact_list=[]):
        customer_post = CustomerPostSerializer()
        customer_post.name = name
        customer_post.identifier = identifier
        customer_post.address_1 = address_1
        customer_post.address_2 = address_2
        customer_post.city = city
        customer_post.state = state
        customer_post.zip_code = zip_code
        customer_post.contact_list = contact_list
        return customer_post

    def test_creation(self):
        cp = self.create()
        assert isinstance(cp, CustomerPostSerializer) is True


class TestCustomerPostResponseSerializer:
    def create(self, customer_uuid=uuid4()):
        customer_post_response = CustomerPostResponseSerializer()
        customer_post_response.customer_uuid = customer_uuid
        return customer_post_response

    def test_creation(self):
        cpr = self.create()
        assert isinstance(cpr, CustomerPostResponseSerializer) is True


class TestCustomerPatchSerializer:
    def create(self, name='jimmyjohns', identifier='id', address_1='123 Street Street', address_2='456 Road Way', city='Citysburg', state='New Kansas', zip_code='12345', contact_list=[]):
        customer_patch = CustomerPatchSerializer()
        customer_patch.name = name
        customer_patch.identifier = identifier
        customer_patch.address_1 = address_1
        customer_patch.address_2 = address_2
        customer_patch.city = city
        customer_patch.state = state
        customer_patch.zip_code = zip_code
        customer_patch.contact_list = contact_list
        return customer_patch

    def test_creation(self):
        cp = self.create()
        assert isinstance(cp, CustomerPatchSerializer) is True


class TestCustomerPatchResponseSerializer:
    def create(self, customer_uuid=uuid4(), name='JimmyJohns', identifier='id', address_1='123 Street Street', address_2='456 Road Way', city='Citysburg', state='New Kansas', zip_code='12345', contact_list=[], created_by='Creator', cb_timestamp=datetime(1234, 5, 6), last_updated_by='Updater', lub_timestamp=datetime(9876, 5, 4)):
        customer_patch_response = CustomerPatchResponseSerializer()
        customer_patch_response.customer_uuid = customer_uuid
        customer_patch_response.name = name
        customer_patch_response.identifier = identifier
        customer_patch_response.address_1 = address_1
        customer_patch_response.address_2 = address_2
        customer_patch_response.city = city
        customer_patch_response.state = state
        customer_patch_response.zip_code = zip_code
        customer_patch_response.contact_list = contact_list
        customer_patch_response.created_by = created_by
        customer_patch_response.cb_timestamp = cb_timestamp
        customer_patch_response.last_updated_by = last_updated_by
        customer_patch_response.lub_timestamp = lub_timestamp
        return customer_patch_response

    def test_creation(self):
        cpr = self.create()
        assert isinstance(cpr, CustomerPatchResponseSerializer) is True


class TestCustomerDeleteResponseSerializer:
    def create(self, customer_uuid=uuid4()):
        customer_delete_response = CustomerDeleteResponseSerializer()
        customer_delete_response.customer_uuid = customer_uuid
        return customer_delete_response

    def test_creation(self):
        cdr = self.create()
        return isinstance(cdr, CustomerDeleteResponseSerializer) is True
