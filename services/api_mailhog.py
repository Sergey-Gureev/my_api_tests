from packages.restclient.configuration import Configuration
from clients.http.api_mailhog.apis.mailhog_api import MailhogAPI


class MaiHogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mail_api = MailhogAPI(configuration=self.configuration)
