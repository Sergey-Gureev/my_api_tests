import json
import time

from email.header import decode_header

import allure

from clients.http.dm_api_account.models.change_registered_user_email import ChangeUserEmail
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_user_passwrord import ResetUserPassword, ChangeUserPassword
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

    @allure.step('auth user')
    def auth_client(self, login, password, remember_me=True, return_model=False ):
        response = self.user_login(login, password, remember_me, return_model=return_model)
        assert response.headers.get("x-dm-auth-token"), 'x-dm-auth-token were not returned'
        x_dm_auth_token = {
            "X-Dm-Auth-Token": f'{response.headers["x-dm-auth-token"]}'
        }
        self.dm_account_api.account_api.set_headers(x_dm_auth_token)
        self.dm_account_api.login_api.set_headers(x_dm_auth_token)

    @allure.step('register new user')
    def register_new_user(self, login, email, password):
        registration_initialized_object = Registration(
            login=login,
            email=email,
            password=password
        )
        register_response = self.dm_account_api.account_api.post_v1_account(registration_initialized_object)
        # assert register_response.status_code in [200, 201]
        return register_response

    @allure.step('activate registered user')
    def activate_registered_user(self,login):
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "response took more than 3 seconds"
        assert token is not None, 'there is no email with your token'

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code in [200, 201]
        assert response.json()['resource']['rating']['enabled'] == True, "user not activated"
        return response

    @allure.step('login user')
    def user_login(self, login, password, remember_me=True, return_model=False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            return_model=return_model
        )
        if not return_model:
            assert response.status_code in [200, 201], f"actual response code = {response.status_code}"
        return response

    @retry(stop_max_attempt_number=4, retry_on_result=retry_if_result_none, wait_fixed=2000)
    @allure.step('get activation token in mailhog')
    def get_activation_token_by_login(self, login, restore_password=False):
        token = None
        mailhog_response = self.mailhog.mail_api.get_api_v2_messages()
        assert mailhog_response.status_code in [200], "mailhog response failed"

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

    @allure.step('change email')
    def change_email(self, login, password, new_email):
        change_users_email = ChangeUserEmail(login=login, password=password, email=new_email)
        self.dm_account_api.account_api.put_v1_account_email(change_users_email=change_users_email)
        token = self.get_activation_token_by_login(login=login)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "email has not been changed"

    @allure.step('change password')
    def change_password(self,login,email, password, new_password):
        # initialize pydandic model user_reset_password
        user_reset_password = ResetUserPassword(
            login = login,
            email = email
        )
        response = self.dm_account_api.account_api.post_v1_account_password(user_reset_password=user_reset_password, validate_response=True)
        assert response.resource.login
        #get token/confirmation for reset password from email:
        token = self.get_activation_token_by_login(login=login, restore_password=True)

        user_change_password= ChangeUserPassword(
            login=login,
            token=token,
            oldPassword=password,
            newPassword=new_password
        )

        response = self.dm_account_api.account_api.put_v1_account_password(changes_users_password=user_change_password)
        assert response.status_code == 200, f"password has not been changed; response errors {response.get('errors')}"

    @allure.step('delete auth user')
    def delete_auth_user(self, all_devices=False, **kwargs):
        if all_devices:
            response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
            assert response.status_code == 204, f"user were not removed. Actual status code {response.status_code}"
            return
        response = self.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, f"user were not removed. Actual status code {response.status_code}"
