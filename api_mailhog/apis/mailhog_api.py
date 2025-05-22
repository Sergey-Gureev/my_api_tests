

from restclient.client import RestClient


class MaihogAPI(RestClient):


    def get_api_v2_messages(self, limit=50):
        """
        Get user's emails
        :param limit:
        :return:
        """
        params = {
            'limit': limit
        }
        response = self.get(
            path=f"/api/v2/messages",
            params = params
        )
        return response