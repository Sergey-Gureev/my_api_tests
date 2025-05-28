import json



def test_post_v1_account(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.user_login(json_data=json_data)

