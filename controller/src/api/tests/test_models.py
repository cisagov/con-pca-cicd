from api.models.customer_models import CustomerContactModel

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