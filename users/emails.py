from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import email_validation_token
from api_app.settings import EMAIL_VALIDATION_FROM, EMAIL_VALIDATION_SUBJECT, \
    PWA_DOMAIN, RESET_PASSWORD_EMAIL_FROM, RESET_PASSWORD_EMAIL_SUBJECT
from core.clients import NotificationsClient


class EmailValidation:
    notifications_client = NotificationsClient()

    def send(self, user):
        data = self._generate_validation_data(user)
        self.notifications_client.send_email_validation(data)

    @staticmethod
    def _generate_validation_data(user):
        return {
            'email': user.email,
            'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': email_validation_token.make_token(user),
            'domain': PWA_DOMAIN
        }


class ResetPasswordEmail:
    notifications_client = NotificationsClient()

    def send(self, user):
        data = self.get_validation_message(user)
        return self.notifications_client.send_email_reset_password(data)

    @staticmethod
    def get_validation_message(user):
        return {
            'email': user.email,
            'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': email_validation_token.make_token(user),
            'domain': PWA_DOMAIN
        }
