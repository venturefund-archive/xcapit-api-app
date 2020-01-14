from .models import Referral


def referral_update(referral_code, email):
    if referral_code and email:
        try:
            referral_id = referral_code
            referral = Referral.objects.get(email=email,
                                            referral_id=referral_id)
            referral.accepted = True
            referral.save()
        except Referral.DoesNotExist:
            # TODO en caso de no existir, se debería crear 🤔
            pass
