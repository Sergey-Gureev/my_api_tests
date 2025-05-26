
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


    def post_v1_account(self, login, email, password, **kwargs):
        """
        Register user
        :param json_data: should contain login, email, password:
        :return: api response
        """

        response = self.post(
            path=f"/v1/account",
            json= {
                "login": login,
                "password": password,
                "email": email
            },
            **kwargs
        )
        return response

    def put_v1_account_token(self, token, **kwargs):
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
            headers=headers,
            **kwargs
        )
        return response

    def put_v1_account_email(self, login, password, new_email, **kwargs):
        """
        Change registered user email
        :param login, password, new_email
        :return: response
        """
        response = self.put(
            path=f"/v1/account/email",
            json = {
                "login": login,
                "password": password,
                "new_email": new_email
            },
            **kwargs
        )
        return response

    def put_v1_account_password(self,json_data, **kwargs):
        """
        Change registered user password
        :param json_data: login,  password, new_password,token: registered user token
        :return:
        """
        response = self.put(
            path=f"/v1/account/password",
            json=json_data,
            # headers=self.session.headers,
            **kwargs
        )
        return response

    def post_v1_account_password(self, json_data, **kwargs):
        """
        Reset registered user password -> should receive confirmation email
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response