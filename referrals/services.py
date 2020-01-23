from .models import Referral


def referral_update(referral_code, email):
    if referral_code and email:
        try:
            referral = Referral.objects.get(email=email,
                                            referral_id=referral_code)
            referral.accepted = True
            referral.save()
        except Referral.DoesNotExist:
            # en caso de no existir, se debe crear
            Referral.objects.create(
                referral_id=referral_code,
                email=email,
                accepted=True
            )
