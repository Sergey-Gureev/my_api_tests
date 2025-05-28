from collections import namedtuple
from datetime import datetime

import pytest

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MaihogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration
from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount

@pytest.fixture
def mailhog():
    mailhog_configuration = MaihogConfiguration(host='http://5.63.153.31:5025',disable_log=True)
    mail_api = MaiHogApi(configuration=mailhog_configuration)
    return mail_api

@pytest.fixture
def account():
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051',disable_log=False)
    account_api = DMApiAccount(configuration=dm_api_configuration)
    return account_api

@pytest.fixture
def account_helper(account, mailhog):
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    return account_helper

@pytest.fixture
def auth_account_helper(mailhog):
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account_api = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog)
    json_data = {
        "login":  f"test.testovichev.{3}",
        "password":  '123456789'
    }
    account_helper.auth_client(json_data=json_data)
    return account_helper

@pytest.fixture(
    scope="function"
)
def prepared_user():
    now = datetime.now()
    # date = now.strftime("%d_%m_%Y_%H_%M_%S")
    date = int(now.timestamp())
    login = f"test.testovichev.{date}"
    password = '123456789'
    email = f"{login}@mail.ru"
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
