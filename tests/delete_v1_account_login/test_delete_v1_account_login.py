

def test_delete_v1_account_login(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.register_and_activate_new_user(json_data=json_data)
    account_helper.auth_client(json_data=json_data)
    account_helper.delete_auth_user()

def delete_v1_account_login_all(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.register_and_activate_new_user(json_data=json_data)
    account_helper.auth_client(json_data=json_data)
    account_helper.delete_auth_user(all_devices=True)