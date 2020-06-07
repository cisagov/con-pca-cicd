import pytest
from unittest import mock


@mock.patch("api.utils.db_utils.get_list")
@pytest.mark.django_db
def test_get(mocked_get_list, client):
    response = client.get("/api/v1/customers/")
    assert mocked_get_list.assert_called


def test_post():
    return
