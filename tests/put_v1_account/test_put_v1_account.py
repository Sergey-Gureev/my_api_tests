# TODO   2.2 в файле put_v1_account_password
#
#         - Регистрация пользователя | copy from test_POST_v1_account
#
#         - Авторизация пользователя | copy from test_POST_v1_account
#
#         - Смена пароля с пробросом авторизационного токена в хэдэры и указанием токена для сброса


def test_change_user_password(account_helper, registered_user):

    account_helper.activate_registered_user(login=registered_user.login)
    account_helper.change_password(
        login=registered_user.login,
        password=registered_user.password,
        email=registered_user.email,
        new_password=f"changed_{registered_user.password}"
    )
