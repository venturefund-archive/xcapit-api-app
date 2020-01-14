from api_app.settings import REFERRAL_EMAIL_FROM, \
    REFERRAL_EMAIL_SUBJECT, PWA_DOMAIN
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text


class ReferralEmail:

    @staticmethod
    def send(user, email):
        message = ReferralEmail.get_referral_message(user, email)
        send_mail(
            REFERRAL_EMAIL_SUBJECT,
            message,
            REFERRAL_EMAIL_FROM,
            [email],
            fail_silently=False,
        )

    @staticmethod
    def get_referral_message(user, email):
        return render_to_string('referral_email.html', {
            'email': email,
            'encode_email': force_text(urlsafe_base64_encode(force_bytes(email))),
            'user_email': user.email,
            'referral_code': user.referral_id,
            'domain': PWA_DOMAIN
        })
