

def test_delete_v1_account_login(auth_account_helper, prepared_user):
    auth_account_helper.delete_auth_user()

def delete_v1_account_login_all(auth_account_helper, prepared_user):
    auth_account_helper.delete_auth_user(all_devices=True)