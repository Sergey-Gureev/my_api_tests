
from restclient.client import RestClient


class LoginAPI(RestClient):

    def delete_v1_account_login(self):
        response = self.delete(path='/v1/account/login')
        return response

    def delete_v1_account_login_all(self, **kwargs):
        response = self.delete(path='/v1/account/login/all',**kwargs)
        return response

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data: login, password, remember_me
        :return:
        """
        response = self.post(
            path=  '/v1/account/login',
            json = json_data
        )
        return response

