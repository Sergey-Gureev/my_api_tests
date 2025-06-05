import datetime

from assertpy import assert_that

# here supposed to be bigger checks
class PostV1Account:

    @classmethod
    def check_registration(cls,response_user_model):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        assert_that(response_user_model.resource.login.startswith(today))