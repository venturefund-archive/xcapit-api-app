import requests
from api_app.settings import API_NOTIFICATIONS


class NotificationsClient:

    @staticmethod
    def _generate_endpoint(last_url_part: str):
        return f'{API_NOTIFICATIONS}{last_url_part}'

    def send_email_validation(self, data):
        endpoint = self._generate_endpoint('send-email-validation/')
        return requests.post(endpoint, json=data)

