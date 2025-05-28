import json

import structlog.processors


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

def test_post_v1_account(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.register_and_activate_new_user(json_data=json_data)
    account_helper.user_login(json_data=json_data)

def test_change_email(account_helper,prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.register_and_activate_new_user(json_data=json_data)
    # changing the email
    new_email = f"changed.{prepared_user.email}"
    account_helper.change_email(json_data=json_data)
    print('new email: ', new_email)