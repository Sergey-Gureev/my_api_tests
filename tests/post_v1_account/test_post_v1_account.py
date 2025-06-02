import hamcrest
import pytest
import requests
from requests import HTTPError

from dm_api_account.models.registration import Registration
from contextlib import contextmanager

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

@pytest.mark.parametrize("field,value", [
    ("password", "12345"),
    ("email", "test.mail.ru"),
    ("login", 'a')])
def test_post_v1_account_negative_params(field, value, prepared_user, account_helper):
    with check_status_code_http(400, "Validation failed"):
        print("\nfield:", field)
        my_dict = {"login": prepared_user.login, "email": prepared_user.email, "password": "12345"}
        my_dict[f"{field}"] = value
        print("my_dict:", my_dict)

        registration_initialized_object = Registration(
                login=my_dict["login"],
                email=my_dict["email"],
                password= my_dict["password"]
            )
        here_error_should_happen = account_helper.register_new_user(registration_initialized_object)
