import time
from collections import namedtuple
from datetime import datetime

import pytest
from pathlib import Path
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration
from services.api_mailhog import MaiHogApi
from services.dm_api_account import DMApiAccount
from vyper import v
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
options = (
    "service.dm_api_account",
    "service.mailhog",
    "user.login",
    "user.password"
)
@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"--env", request.config.getoption(f"--{option}"))

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)

@pytest.fixture
def mailhog():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=True)
    mail_api = MaiHogApi(configuration=mailhog_configuration)
    return mail_api

@pytest.fixture
def account():
    dm_api_configuration = DMmApiConfiguration(host=v.get("service.dm_api_account"),disable_log=False)
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
    _login = v.get("user.login")
    login = f"{_login}+{date}"
    password = v.get("user.password")
    email = f"{login}@mail.ru"
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
