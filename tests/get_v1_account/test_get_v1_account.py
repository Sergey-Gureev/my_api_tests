from hamcrest import assert_that, has_property, contains_string, has_items

from dm_api_account.models.user_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    assert response.resource.login
    print(response.resource)
    assert_that(response, has_property("resource", has_property("login", contains_string('testovich'))))
    assert_that(response.resource.roles, has_items("Guest", "Player"))

def test_get_v1_account_no_auth(account_helper):
    response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    assert response.status_code == 401, "should not get unauthorized user but did"

