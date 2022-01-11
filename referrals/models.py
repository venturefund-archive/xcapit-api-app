from django.db import models
from users.models import User

CLAIM_STATUS = [
    ('claimed', 'claimed'),
    ('delivered', 'delivered')
]


class Referral(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    referral_id = models.CharField(max_length=250)


class Campaign(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True)
    name = models.CharField(max_length=200)


class Claim(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='claims', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='referral_claims', on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'campaign')


class ClaimStatus(models.Model):
    claim = models.ForeignKey(Claim, related_name='claim_statuses', on_delete=models.PROTECT)
    status = models.CharField(choices=CLAIM_STATUS, max_length=100)
    date = models.DateTimeField(auto_now=True)
