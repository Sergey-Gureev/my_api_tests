import requests
# from hamcrest import assert_that, has_property, contains_string, has_items
from requests.exceptions import HTTPError
from contextlib import contextmanager
from assertpy import assert_that, soft_assertions


@contextmanager
def check_status_code_http(expected_status_code: requests.codes, expected_message: str = ""):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Expected status_code should be equal {expected_status_code}")
        if expected_message:
            raise AssertionError(f"expected to get error message '{expected_message}' but got response without error")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http(200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    assert response.resource.login
    print(response.resource)
    assert_that(response, has_property("resource", has_property("login", contains_string('testovich'))))
    assert_that(response.resource.roles, has_items("Guest", "Player"))

def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    # assert response.status_code == 401, "should not get unauthorized user but did"

