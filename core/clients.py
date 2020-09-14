import requests
from api_app.settings import API_NOTIFICATIONS


class NotificationsClient:

    @staticmethod
    def _generate_endpoint(last_url_part: str):
        return f'{API_NOTIFICATIONS}{last_url_part}'

    def send_email_validation(self, data):
        endpoint = self._generate_endpoint('notifications/send-email-validation/')
        return requests.post(endpoint, json=data)

    def send_referral_email(self, data: dict) -> requests.Response:
        endpoint = self._generate_endpoint('notifications/send-referral-email/')
        return requests.post(endpoint, json=data)

    def send_email_reset_password(self, data):
        endpoint = self._generate_endpoint('notifications/send-email-reset-password/')
        return requests.post(endpoint, json=data)

