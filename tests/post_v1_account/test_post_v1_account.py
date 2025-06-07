import datetime

import allure
import pytest
from assertpy import assert_that

from checkers.checker_post_v1_account import PostV1Account
from checkers.checkers import check_status_code_http


@allure.suite('tests for post v1 account endpoint')
class TestPostV1Account:
    @allure.sub_suite('negative tests for register user, register with non-valid param')
    @pytest.mark.parametrize(
        'login, email, password',
        [
            pytest.param('ek-n-pavlova', 'ek-n-pavlova@mail.ru', '12345', id='invalid_password'),
            pytest.param('ek-n-pavlova', 'ek-n-pavlovamail.ru', '123456789', id='invalid_email'),
            pytest.param('e', 'ek-n-pavlova@mail.ru', '123456789', id='invalid_login')
        ])
    def test_post_v1_account_negative_params(self, login, email, password, account_helper):
        with check_status_code_http(400, "Validation failed"):
            here_error_should_happen = account_helper.register_new_user(
                login=login,
                email=email,
                password=password)

    @allure.sub_suite('positive test for register user')
    def test_post_v1_account(self, prepared_user, account_helper):
        response = account_helper.register_new_user(
                login=prepared_user.login,
                email=prepared_user.email,
                password=prepared_user.password)
        assert response.status_code == 201
        account_helper.activate_registered_user(login=prepared_user.login)
        response_user_model = account_helper.user_login(
            login=prepared_user.login,
            password=prepared_user.password,
            return_model=True
        )
        PostV1Account.check_registration(response_user_model)

