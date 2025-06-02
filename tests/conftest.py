import time
from collections import namedtuple
from datetime import datetime

import pytest
from schemathesis.stateful.validation import validate_response

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration
from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount

import structlog.processors


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

@pytest.fixture
def mailhog():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
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
def registered_user(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.activate_registered_user(login=login)
    return prepared_user

@pytest.fixture
def auth_account_helper(account_helper, registered_user):
    account_helper.auth_client(login=registered_user.login,
                               password=registered_user.password,
                               remember_me=True,
                               return_model=False)
    return account_helper

@pytest.fixture(  #function, module, session, class
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
