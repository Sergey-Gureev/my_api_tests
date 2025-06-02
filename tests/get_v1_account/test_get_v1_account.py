from datetime import datetime
from assertpy import assert_that, soft_assertions
from checkers import check_status_code_http
from dm_api_account.models.user_envelope import UserRole



def test_get_v1_account_auth(auth_account_helper, prepared_user):
    with check_status_code_http(200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to(prepared_user.login)
            assert_that(response.resource.online).is_instance_of(datetime)
            assert_that(response.resource.roles).contains(UserRole.PLAYER, UserRole.GUEST)


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)

