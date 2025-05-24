import datetime
import json
from collections import namedtuple

import pytest
import structlog.processors
from requests import session

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MaihogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration

from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount


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


@pytest.fixture(scope="session")
def prepared_user():
    now = datetime.datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f"test.testovichev.{date}"
    password = '123456789'
    email = f"{login}@mail.ru"
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user

def test_post_v1_account(account_helper, prepared_user):
    login = prepared_user.login
    password = prepared_user.password
    email = prepared_user.email
    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login,password=password)

def test_change_email(account_helper,prepared_user):

    # changing the email
    new_email = f"changed.{prepared_user.email}"
    account_helper.change_email(
        login=prepared_user.login,
        password=prepared_user.password,
        new_email= new_email
    )
    print('new email: ', new_email)
