
from restclient.client import RestClient


class Login_API(RestClient):


    def login(self, login, password):
        response = self.post(
            path=  '/v1/account/login',
            json = {
                "login": f"{login}",
                "password": f"{password}",
                "rememberMe": True
            }
        )
        return response