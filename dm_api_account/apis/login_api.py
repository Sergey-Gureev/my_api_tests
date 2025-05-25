
from restclient.client import RestClient


class LoginAPI(RestClient):

    def delete_v1_account_login(self):
        self.delete(path='/v1/account/login')

    def delete_v1_account_login_all(self):
        self.delete(path='/v1/account/login/all')

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

