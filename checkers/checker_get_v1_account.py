from datetime import datetime

import allure
from assertpy import assert_that, soft_assertions
from dm_api_account.models.user_envelope import UserRole

class GetV1AccountChecker:

    @classmethod
    @allure.step('check user fields in response')
    def check_user_params(cls,user_model_response, prepared_user):
        with soft_assertions():
            assert_that(user_model_response.resource.login).is_equal_to(prepared_user.login)
            assert_that(user_model_response.resource.rating.enabled).is_true()
            assert_that(user_model_response.resource.settings.color_schema).is_equal_to("Modern")
            assert_that(user_model_response.resource.online).is_instance_of(datetime)
            assert_that(user_model_response.resource.roles).contains(UserRole.PLAYER, UserRole.GUEST)