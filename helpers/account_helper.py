import json
import time

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MaiHogApi
from retrying import retry

def retry_if_result_none(result):
    return result is None

def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'attempt #{count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("to many attempts")
            if token:
                return token
            time.sleep(1)
    return wrapper

class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MaiHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login:str, password: str, email:str):

        register_response = self.dm_account_api.account_api.post_v1_account(login=login,password=password,email=email)
        assert register_response.status_code in [200, 201]

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, 'there is no email with your token'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.json()['resource']['rating']['enabled'] == True, "user not activated"

        return response

    def user_login(self, login:str, password:str, remember_me: bool=True):
        self.dm_account_api.login_api.post_v1_account_login(login=login,password=password,remember_me=remember_me)

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
        token = None
        mailhog_response = self.mailhog.mail_api.get_api_v2_messages()
        if mailhog_response.status_code == 200:
            for item in mailhog_response.json()['items']:
                if json.loads(item['Content']['Body'])['Login'] == login:
                    token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                    break
        return token
        # assert token is not None, 'there is no email with your token'
    def change_email(self, login, password, new_email):
        self.dm_account_api.account_api.put_v1_account_email(
            login=login,
            password=password,
            new_email=new_email
        )
        token = self.get_activation_token_by_login(login=login)
        self.dm_account_api.account_api.put_v1_account_token(token=token)

        self.user_login(login=login, password=password)

