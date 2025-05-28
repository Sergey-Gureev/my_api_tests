
# TODO 2. Напишите следующие тесты:
# 2.1 в файле get_v1_account.py
# - Получить информацию о пользователе (используя авторизованный клиент)
def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()
