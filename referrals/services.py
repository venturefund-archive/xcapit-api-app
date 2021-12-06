from users.models import User
from .models import Referral


def referral_update(referral_code, email):
    normalized_email = User.objects.normalize_email(email)
    if referral_code and normalized_email:
        try:
            referral = Referral.objects.get(email=normalized_email,
                                            referral_id=referral_code)
            referral.save()
        except Referral.DoesNotExist:
            Referral.objects.create(
                referral_id=referral_code,
                email=normalized_email,
            )


def validate_referral(referral_code, email):
    referral = Referral.objects.get(email=email,
                                    referral_id=referral_code)
    referral.accepted = True
    referral.save()
