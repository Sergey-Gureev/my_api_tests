
from restclient.client import RestClient


class Login_API(RestClient):


    def post_v1_account_login(self, login:str, password:str, remember_me=True):
        response = self.post(
            path=  '/v1/account/login',
            json = {
                "login": f"{login}",
                "password": f"{password}",
                "rememberMe": remember_me
            }
        )
        return response