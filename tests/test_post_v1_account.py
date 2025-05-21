from datetime import datetime
import json
from platform import processor
from pprint import pprint
from time import sleep

import structlog.processors

from account_api.account_api import AccountAPI
from api_mailhog.api.mailhog_api import MaihogAPI
from login_api.login_api import Login_API
from restclient.configuration import Configuration as MaihogConfiguration
from restclient.configuration import Configuration as DMmApiConfiguration


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

def test_post_v1_account():

    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
    }
    login = "test.testovichev.1"
    password = '123456789'
    email = f"{login}@mail.ru"
    mailhog_configuration = MaihogConfiguration(host='http://5.63.153.31:5025',enable_log=False)
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051',enable_log=True)

    account_api = AccountAPI(configuration=dm_api_configuration)
    login_api = Login_API(configuration=dm_api_configuration)
    mailapi = MaihogAPI(configuration=mailhog_configuration)

    # registering new account
    # print('\ninput data: ', login, email)
    register_response = account_api.register_new_user(login=login, email=email, password=password)
    # if 'error' in register_response.text:
    #     print(register_response.json()['errors'])
    assert register_response.status_code in [200, 201]
    sleep(10)

    # getting token for activating account from received email
    # print('getting token...')
    emails = mailapi.get_api_v2_messages()
    token = None
    if emails.status_code == 200:
        for item in emails.json()['items']:
            if json.loads(item['Content']['Body'])['Login']  == login:
                token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                break
    assert token is not None, 'there is no email with your token'
    # print(f'token for email: ',token)

    # Activating account
    # print('Activating...')
    resp = account_api.activate_registered_user(token)
    # print("is_user_activated?: ", resp.json()['resource']['rating']['enabled'])
    assert resp.json()['resource']['rating']['enabled'] == True, "user not activated"

    # Login with activated account
    login_result = login_api.login(login=login, password=password)
    # print("login with activated user", login_result.text)
    assert login_result.status_code == 200

    # changing the email
    new_email = f"changed.{email}"
    response = account_api.change_registered_user_email(
        login=login,
        password=password,
        new_email= new_email
    )
    # print('new email: ', new_email)
    # print('new email response: ', response.json())

    # try login again. Expecting error
    login_result_attempt_2 = login_api.login(login=login, password=password)
    # print("login with CHANGED user", login_result_attempt_2.text)
    assert login_result_attempt_2.status_code != 200

    print('getting new token...')
    sleep(10)
    emails = mailapi.get_api_v2_messages()
    new_token = None
    if emails.status_code == 200:
        for item in emails.json()['items']:
            # print(item['To'][0]['Mailbox'], item)
            if item['To'][0]['Mailbox'] +"@"+ item['To'][0]['Domain'] == new_email:
                print('!!!Found:',item)
                new_token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                break
    assert new_token is not None, 'there is no email with your token'
    print(f'New token from {new_email} email: ', new_token)

    #activating again
    print('Activating again...')
    resp = account_api.activate_registered_user(new_token)
    print(resp.text)
    print("is_user_activated?: ", resp.json()['resource']['rating']['enabled'])
    assert resp.json()['resource']['rating']['enabled'] == True, "user not activated"

    #login again with edited  activated account
    login_result = login_api.login(login=login, password=password)
    print("\nlogin with edited activated user", login_result.text)
    assert login_result.status_code == 200