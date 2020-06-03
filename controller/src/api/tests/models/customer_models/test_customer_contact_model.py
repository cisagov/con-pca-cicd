from api.models.customer_models import CustomerContactModel


customer_contact_model_data = {
    "first_name": "Ronald",
    "last_name": "McDonald",
    "title": "Farmer",
    "office_phone": "123-456-7890",
    "mobile_phone": "123-456-7891",
    "email": "ronald.mcdonald@test.com",
    "notes": "some notes",
}

# add validation to fields
def test_creation():
    cc = CustomerContactModel(customer_contact_model_data)
    assert isinstance(cc, CustomerContactModel) is True
