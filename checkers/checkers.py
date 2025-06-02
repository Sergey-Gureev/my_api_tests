import requests
from requests import HTTPError

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