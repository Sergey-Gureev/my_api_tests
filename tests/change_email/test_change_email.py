
def test_change_email(auth_account_helper,prepared_user):
    # changing the email
    new_email = f"changed.{prepared_user.email}"
    auth_account_helper.change_email(login=prepared_user.login, password=prepared_user.password, new_email=new_email)
