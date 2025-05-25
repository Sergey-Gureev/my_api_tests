# TODO   2.2 в файле put_v1_account_password
#
#         - Регистрация пользователя | copy from test_POST_v1_account
#
#         - Авторизация пользователя | copy from test_POST_v1_account
#
#         - Смена пароля с пробросом авторизационного токена в хэдэры и указанием токена для сброса


def test_change_user_password(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.register_and_activate_new_user(json_data=json_data)

    account_helper.change_password(
        login=prepared_user.login,
        password=prepared_user.password,
        email=prepared_user.email,
        new_password=f"changed_{prepared_user.password}"
    )
