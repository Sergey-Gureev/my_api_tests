import json

import structlog.processors
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MaihogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration

from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount

def test_post_v1_account(account_helper, prepared_user):
    json_data = {
        "login": prepared_user.login,
        "password": prepared_user.password,
        "email": prepared_user.email
    }
    account_helper.user_login(json_data=json_data)

