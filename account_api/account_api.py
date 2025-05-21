
from restclient.client import RestClient


class AccountAPI(RestClient):

    def register_new_user(self, login, email, password):
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

    def activate_registered_user(self, token):
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

    def change_registered_user_email(self,login, password, new_email):
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
