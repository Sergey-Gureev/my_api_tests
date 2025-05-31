import json

import structlog.processors
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MaihogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration

from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount

def test_post_v1_account(registered_user, account_helper):
    account_helper.user_login(login=registered_user.login, password=registered_user.password, remember_me=True)

