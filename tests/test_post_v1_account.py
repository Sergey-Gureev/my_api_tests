import json
from time import sleep

import structlog.processors

from dm_api_account.apis.account_api.account_api import AccountAPI
from api_mailhog.api.mailhog_api import MaihogAPI
from dm_api_account.apis.login_api.login_api import Login_API
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

    login = "test.testovichev.7"
    password = '123456789'
    email = f"{login}@mail.ru"
    mailhog_configuration = MaihogConfiguration(host='http://5.63.153.31:5025',disable_log=True)
    dm_api_configuration = DMmApiConfiguration(host='http://5.63.153.31:5051',disable_log=False)

    account_api = AccountAPI(configuration=dm_api_configuration)
    login_api = Login_API(configuration=dm_api_configuration)
    mailapi = MaihogAPI(configuration=mailhog_configuration)

    print("\nregistering new account")
    register_response = account_api.post_v1_account(login=login, email=email, password=password)
    assert register_response.status_code in [200, 201]

    print('\ngetting token...1st')
    emails = mailapi.get_api_v2_messages()
    token = None
    if emails.status_code == 200:
        for item in emails.json()['items']:
            if json.loads(item['Content']['Body'])['Login']  == login:
                token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                break
    assert token is not None, 'there is no email with your token'

    print('Activating...')
    resp = account_api.put_v1_account_token(token)
    assert resp.json()['resource']['rating']['enabled'] == True, "user not activated"

    login_result = login_api.login(login=login, password=password)
    print("login with activated user", login_result.text)
    assert login_result.status_code == 200

    # changing the email
    new_email = f"changed.{email}"
    response = account_api.put_v1_account_email(
        login=login,
        password=password,
        new_email= new_email
    )
    # print('new email: ', new_email)
    print('new email response: ', response.json())

    # try login again. Expecting error
    login_result_attempt_2 = login_api.login(login=login, password=password)
    print("login with CHANGED user", login_result_attempt_2.text)
    assert login_result_attempt_2.status_code != 200

    print('getting new token for CHANGED email')
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
    print(f'New token from CHANGED {new_email} email: ', new_token)

    #activating again
    print('Activating again... CHANGED')
    resp = account_api.put_v1_account_token(new_token)
    print(resp.text)
    print("is_user_activated?: ", resp.json()['resource']['rating']['enabled'])
    assert resp.json()['resource']['rating']['enabled'] == True, "user not activated"

    #login again with edited  activated account
    login_result = login_api.login(login=login, password=password)
    print("\nlogin with CHANGED activated user", login_result.text)
    assert login_result.status_code == 200