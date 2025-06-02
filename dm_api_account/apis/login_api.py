from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginAPI(RestClient):

    def delete_v1_account_login(self):
        response = self.delete(path='/v1/account/login')
        return response

    def delete_v1_account_login_all(self, **kwargs):
        response = self.delete(path='/v1/account/login/all',**kwargs)
        return response

    def post_v1_account_login(self, login_credentials: LoginCredentials, return_model=True):
        """
        Authenticate via credentials
        :param login_credentials: login, password, remember_me
        :param return_model: pydantic validation flag -> if true return User object
        :return:
        """
        response = self.post(
            path=  '/v1/account/login',
            json = login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if return_model:
            return UserEnvelope(**response.json()) # gives opportunity to reach user properties as object.properties
        return response

