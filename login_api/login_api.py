import requests

class Login_API():
    def __init__(self, host, headers=[]):
        self.host = host
        self.headers = headers

    def login(self, login, password):
        response = requests.post(
            url=  'http://5.63.153.31:5051/v1/account/login',
            json = {
                "login": f"{login}",
                "password": f"{password}",
                "rememberMe": True
            }
        )
        return response