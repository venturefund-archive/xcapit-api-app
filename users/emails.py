from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import email_validation_token

from api_app.settings import EMAIL_VALIDATION_FROM, EMAIL_VALIDATION_SUBJECT, \
    PWA_DOMAIN, RESET_PASSWORD_EMAIL_FROM, RESET_PASSWORD_EMAIL_SUBJECT


class EmailValidation:

    @staticmethod
    def send(user):
        message = EmailValidation.get_validation_message(user)
        send_mail(
            EMAIL_VALIDATION_SUBJECT,
            message,
            EMAIL_VALIDATION_FROM,
            [user.email],
            fail_silently=False,
        )

    @staticmethod
    def get_validation_message(user):
        return render_to_string('email_validation.html', {
            'email': user.email,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': email_validation_token.make_token(user),
            'domain': PWA_DOMAIN
        })


class ResetPasswordEmail:

    @staticmethod
    def send(user):
        message = ResetPasswordEmail.get_validation_message(user)
        send_mail(
            RESET_PASSWORD_EMAIL_SUBJECT,
            message,
            RESET_PASSWORD_EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )

    @staticmethod
    def get_validation_message(user):
        return render_to_string('reset_password_email.html', {
            'email': user.email,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': email_validation_token.make_token(user),
            'domain': PWA_DOMAIN
        })
