import pytest

from checkers.checkers import check_status_code_http


@pytest.mark.parametrize(
    'login, email, password',
    [
        pytest.param('ek-n-pavlova', 'ek-n-pavlova@mail.ru', '12345', id='invalid_password'),
        pytest.param('ek-n-pavlova', 'ek-n-pavlovamail.ru', '123456789', id='invalid_email'),
        pytest.param('e', 'ek-n-pavlova@mail.ru', '123456789', id='invalid_login')
    ])
def test_post_v1_account_negative_params(login, email, password, account_helper):
    with check_status_code_http(400, "Validation failed"):
        here_error_should_happen = account_helper.register_new_user(
            login=login,
            email=email,
            password=password)
