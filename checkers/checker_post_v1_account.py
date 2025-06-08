import datetime

import allure
from assertpy import assert_that

# here supposed to be bigger checks
class PostV1Account:

    @classmethod
    @allure.step('check registration field in response')
    def check_registration(cls,response_user_model):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        assert_that(response_user_model.resource.login.startswith(today))