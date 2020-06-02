from api.models.customer_models import CustomerContactModel
from api.models.customer_models import CustomerModel
from uuid import uuid4
from datetime import datetime


class TestCustomerContactModel:
    def create(self, first_name='Ronald', last_name='McDonald', title='Farmer', office_phone='123-456-7890', mobile_phone='123-456-7891', email='ronald.mcdonald@test.com', notes='Some Notes'):
        customer_contact = CustomerContactModel()
        customer_contact.first_name = first_name
        customer_contact.last_name = last_name
        customer_contact.title = title
        customer_contact.office_phone = office_phone
        customer_contact.mobile_phone = mobile_phone
        customer_contact.email = email
        customer_contact.notes = notes
        return customer_contact

    # add validation to fields
    def test_creation(self):
        cc = self.create()
        assert isinstance(cc, CustomerContactModel) is True


class TestCustomerModel:
    def create(self, customer_uuid=str(uuid4()), name='McDonalds', identifier='id', address_1='123 Street Street', address_2='456 Road Way', city='Citysburg', state='New Kansas', zip_code='12345', contact_list=[], created_by='Creator', cb_timestamp=datetime(1234, 5, 6), last_update_by='Updater', lub_timestamp=datetime(7890, 1, 2)):
        customer = CustomerModel()
        customer.customer_uuid = customer_uuid
        customer.name = name
        customer.identifier = identifier
        customer.address_1 = address_1
        customer.address_2 = address_2
        customer.city = city
        customer.state = state
        customer.zip_code = zip_code
        customer.contact_list = contact_list
        customer.created_by = created_by
        customer.cb_timestamp = cb_timestamp
        customer.last_updated_by = last_update_by
        customer.lub_timestamp = lub_timestamp
        return customer

    # add validation to fields
    def test_creation(self):
        c = self.create()
        assert isinstance(c, CustomerModel) is True
