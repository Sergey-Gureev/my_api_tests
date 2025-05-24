import json

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MaiHogApi

class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MaiHogApi):
        self.dm_account_api = dm_account_api
        self.maihog = mailhog

    def register_new_user(self, login:str, password: str, email:str):

        register_response = self.dm_account_api.account_api.post_v1_account(login=login,password=password,email=email)
        assert register_response.status_code in [200, 201]

        mailhog_response = self.maihog.mail_api.get_api_v2_messages()
        token = self.get_activation_token_by_login(login=login,mailhog_response=mailhog_response)
        assert token is not None, 'there is no email with your token'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.json()['resource']['rating']['enabled'] == True, "user not activated"

        return response

    def user_login(self, login:str, password:str, remember_me: bool=True):
        self.dm_account_api.login_api.post_v1_account_login(login=login,password=password,remember_me=remember_me)

    @staticmethod
    def get_activation_token_by_login(login, mailhog_response):
        token = None
        if mailhog_response.status_code == 200:
            for item in mailhog_response.json()['items']:
                if json.loads(item['Content']['Body'])['Login'] == login:
                    token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                    break
        return token
        # assert token is not None, 'there is no email with your token'



