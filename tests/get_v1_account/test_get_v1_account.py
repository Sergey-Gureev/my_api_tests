

from checkers.checker_get_v1_account import GetV1AccountChecker
from checkers.checkers import check_status_code_http



def test_get_v1_account_auth(auth_account_helper, prepared_user):
    with check_status_code_http(200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
        GetV1AccountChecker.check_user_params(user_model_response=response, prepared_user=prepared_user)

def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)

