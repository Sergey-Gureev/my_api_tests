
from restclient.client import RestClient


class AccountAPI(RestClient):

    def get_v1_account(self, **kwargs):
        """
        get user
        """

        response = self.get(
            headers=self.session.headers,
            path=f"/v1/account",
            **kwargs
        )
        return response


    def post_v1_account(self, json_data):
        """
        Register user
        :param json_data: should contain login, email, password:
        :return: api response
        """
        response = self.post(
            headers=self.session.headers,
            path=f"/v1/account",
            json=json_data
        )
        return response

    def put_v1_account_token(self, token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            "accept": "text/plain",
        }
        response = self.put(
            path=f"/v1/account/{token}",
            headers=headers
        )
        return response

    def put_v1_account_email(self, json_data):
        """
        Change registered user email
        :param json_data should include login, password, new_email
        :return: response
        """
        response = self.put(
            path=f"/v1/account/email",
            json = json_data
        )
        return response

    def put_v1_account_password(self, login, password, new_password, token):
        """
        Change registered user password
        :param login:
        :param password:
        :param new_password:
        :param token: registered user token
        :return:
        """
        data = {
            "login": f"{login}",
            "token": f"{token}",
            "oldPassword": f"{password}",
            "newPassword": f"{new_password}"
        }
        response = self.put(
            path=f"/v1/account/password",
            json=data,
            headers=self.session.headers,
        )
        return response

    def post_v1_account_password(self, json_data):
        """
        Reset registered user password -> should receive confirmation email
        :return:
        """
        self.post(
            path='/v1/account/password',
            json=json_data,

        )