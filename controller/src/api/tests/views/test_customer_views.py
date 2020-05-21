import pytest
import mock


class TestCustomerListView:

    @mock.patch('api.utils.db_utils.get_list')
    @pytest.mark.django_db
    def test_get(self, mocked_get_list, client):
        response = client.get('/api/v1/customers/')
        print(dir(mocked_get_list))
        assert mocked_get_list.assert_called

    def test_post(self):
        return

