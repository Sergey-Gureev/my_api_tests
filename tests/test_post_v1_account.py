import json

import structlog.processors
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

def test_post_v1_account():

    login = "test.testovichev.21"
    password = '123456789'
    email = f"{login}@mail.ru"
    mailhog_configuration = MaihogConfiguration(host='http://5.63.153.31:5025',disable_log=True)
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051',disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailapi = MaiHogApi(configuration=mailhog_configuration)
    account_helper =   AccountHelper(dm_account_api=account, mailhog=mailapi)

    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login,password=password)

def test_change_email():
    login = "test.testovichev.13"
    password = '123456789'
    email = f"{login}@mail.ru"
    mailhog_configuration = MaihogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailapi = MaiHogApi(configuration=mailhog_configuration)
    # changing the email
    new_email = f"changed.{email}"
    response = account.account_api.put_v1_account_email(
        login=login,
        password=password,
        new_email= new_email
    )
    # print('new email: ', new_email)
    print('new email response: ', response.json())

    # try login again. Expecting error
    login_result_attempt_2 = account.login_api.post_v1_account_login(login=login, password=password)
    print("login with CHANGED user", login_result_attempt_2.text)
    assert login_result_attempt_2.status_code != 200

    print('getting new token for CHANGED email')
    emails = mailapi.mail_api.get_api_v2_messages()
    new_token = None
    if emails.status_code == 200:
        for item in emails.json()['items']:
            # print(item['To'][0]['Mailbox'], item)
            if item['To'][0]['Mailbox'] +"@"+ item['To'][0]['Domain'] == new_email:
                print('!!!Found:',item)
                new_token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                break
    assert new_token is not None, 'there is no email with your token'
    print(f'New token from CHANGED {new_email} email: ', new_token)

    #activating again
    print('Activating again... CHANGED')
    resp = account.account_api.put_v1_account_token(new_token)
    print(resp.text)
    print("is_user_activated?: ", resp.json()['resource']['rating']['enabled'])
    assert resp.json()['resource']['rating']['enabled'] == True, "user not activated"

    #login again with edited  activated account
    login_result = account.login_api.post_v1_account_login(login=login, password=password)
    print("\nlogin with CHANGED activated user", login_result.text)
    assert login_result.status_code == 200