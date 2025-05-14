import requests

class AccountAPI:
    def __init__(self, host, headers):
        self.host = host
        self.headers = headers

    def register_new_user(self, login, email, password):
        """
        Register new user
        :param login:
        :param email
        :param password:
        :return:
        """

        response = requests.post(
            headers=self.headers,
            url=f"{self.host}/v1/account",
            json={
                "login": f"{login}",
                "email": f"{email}",
                "password": f"{password}",
            }
        )
        return response

    def activate_registered_user(self, token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            "accept": "text/plain",
        }
        response = requests.put(
            url=f"{self.host}/v1/account/{token}",
            headers=headers
        )
        return response

    def change_registered_user_email(self,login, password, new_email):
        data = {
            "login": f"{login}",
            "password": f"{password}",
            "email": f"{new_email}"
}
        response = requests.put(
            url=f"{self.host}/v1/account/email",
            json = data
        )
        return response
