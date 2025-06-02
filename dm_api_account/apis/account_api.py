from dm_api_account.models.change_registered_user_email import ChangeUserEmail
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_user_passwrord import ResetUserPassword, ChangeUserPassword
from dm_api_account.models.user_detail_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountAPI(RestClient):

    def get_v1_account(self, validate_response, **kwargs):
        """
        get user
        """
        response = self.get(
            headers=self.session.headers,
            path=f"/v1/account",
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    def post_v1_account(self, registration: Registration, **kwargs):
        """
        Register user
        :param registration login, email, password
        :return:  api response
        """
        response = self.post(
            path=f"/v1/account",
            json= registration.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response

    def put_v1_account_token(self, token, validate_response=True,**kwargs):
        """
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        """
        headers = {
            "accept": "text/plain",
        }
        response = self.put(
            path=f"/v1/account/{token}",
            headers=headers,
            **kwargs
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_email(self, change_users_email: ChangeUserEmail, validate_response=True, **kwargs):
        """
        Change registered user email to a new email
        :param validate_response:
        :param change_users_email: with login, new_email, password:
        :return:  response
        """
        response = self.put(
            path=f"/v1/account/email",
            json = change_users_email.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(self, changes_users_password: ChangeUserPassword, **kwargs):
        """
        Change registered user password
        :param changes_users_password: pydantic model with login,  password, new_password,token: registered user token
        :return:
        """
        response = self.put(
            path=f"/v1/account/password",
            json=changes_users_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response

    def post_v1_account_password(self, user_reset_password: ResetUserPassword, validate_response=True, **kwargs):
        """
        Reset registered user password -> should receive confirmation email
            :param user_reset_password: login, email
            :param validate_response: pydantic validation flag
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=user_reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response