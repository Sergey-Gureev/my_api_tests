import json
import time

from email.header import decode_header


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
        self.token=None

    def auth_client(self, json_data ):

        response = self.dm_account_api.login_api.post_v1_account_login(json_data)
        x_dm_auth_token = {
            "X-Dm-Auth-Token": f'{response.headers["x-dm-auth-token"]}'
        }
        self.dm_account_api.account_api.set_headers(x_dm_auth_token)
        self.dm_account_api.login_api.set_headers(x_dm_auth_token)


    def register_new_user(self, json_data):
        register_response = self.dm_account_api.account_api.post_v1_account(json_data)
        assert register_response.status_code in [200, 201]

    def activate_registered_user(self,login):
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, 'there is no email with your token'

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.json()['resource']['rating']['enabled'] == True, "user not activated"

        return response

    def user_login(self, json_data):
        self.dm_account_api.login_api.post_v1_account_login(json_data)

    @retry(stop_max_attempt_number=4, retry_on_result=retry_if_result_none, wait_fixed=2000)
    def get_activation_token_by_login(self, login, restore_password=False):
        token = None
        mailhog_response = self.mailhog.mail_api.get_api_v2_messages()
        if mailhog_response.status_code == 200:
            for item in mailhog_response.json()['items']:
                subject = f"{item['Content']['Headers']['Subject'][0]}"
                result = decode_header(subject)
                txt, encoding = result
                subject = txt[0].decode(txt[1])
                print(f"subject: {subject}")
                if restore_password and "Подтверждение сброса пароля" in subject:
                    token = json.loads(item['Content']['Body'])['ConfirmationLinkUri'].split('/')[-1]
                    break
                elif json.loads(item['Content']['Body'])['Login'] == login:
                    token = json.loads(item['Content']['Body'])['ConfirmationLinkUrl'].split('/')[-1]
                    break
        return token
        # assert token is not None, 'there is no email with your token'

    def change_email(self, login, password, new_email):
        self.dm_account_api.account_api.put_v1_account_email(login=login,password=password, new_email=new_email)
        token = self.get_activation_token_by_login(login=login)
        self.dm_account_api.account_api.put_v1_account_token(token=token)

    def change_password(self,login,email, password, new_password):

        # activating registered user
        json_data = {
            "login": login,
            "email": email,
            "password":password
        }
        print("let's authenticate")
        self.auth_client(json_data=json_data)
        # reset password email confirmation:
        print("let's request token for restore password")
        self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        #get token/confirmation for reset password from email:
        token = self.get_activation_token_by_login(login=login, restore_password=True)
        print("token for restore password: "+token)
        print("\n let's change password: ... ")
        json_data.update({"token":token})
        self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)

    def delete_auth_user(self, all_devices=False, **kwargs):
        if all_devices:
            self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
            return
        self.dm_account_api.login_api.delete_v1_account_login()