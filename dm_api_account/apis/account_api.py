
from restclient.client import RestClient


class AccountAPI(RestClient):

    def post_v1_account(self, login, email, password):
        """
        Register user
        :param login:
        :param email:
        :param password:
        :return:
        """

        response = self.post(
            headers=self.headers,
            path=f"/v1/account",
            json={
                "login": f"{login}",
                "email": f"{email}",
                "password": f"{password}",
            }
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

    def put_v1_account_email(self, login, password, new_email):
        """
        Change registered user email
        :param login:
        :param password:
        :param new_email:
        :return:
        """
        data = {
            "login": f"{login}",
            "password": f"{password}",
            "email": f"{new_email}"
}
        response = self.put(
            path=f"/v1/account/email",
            json = data
        )
        return response
