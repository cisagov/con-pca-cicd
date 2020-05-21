import pytest

class TestCustomerListView:

    @pytest.mark.django_db
    def test_get(self, client):
        response = client.get('/v1/customers/')
        print(response)
        return

    def test_post(self):
        return

