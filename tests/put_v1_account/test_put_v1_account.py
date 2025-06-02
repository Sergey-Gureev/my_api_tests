# TODO   2.2 в файле put_v1_account_password
#
#         - Регистрация пользователя | copy from test_POST_v1_account
#
#         - Авторизация пользователя | copy from test_POST_v1_account
#
#         - Смена пароля с пробросом авторизационного токена в хэдэры и указанием токена для сброса


def test_change_user_password(auth_account_helper, prepared_user):
    auth_account_helper.change_password(
        login=prepared_user.login,
        password=prepared_user.password,
        email=prepared_user.email,
        new_password=f"changed_{prepared_user.password}"
    )
    login_with_new_pass_response = auth_account_helper.user_login(
        login=prepared_user.login,
        password=f"changed_{prepared_user.password}")
    assert login_with_new_pass_response.status_code == 200