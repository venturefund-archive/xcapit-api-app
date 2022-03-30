from django.db import models


class Referral(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    referral_id = models.CharField(max_length=250)


class BlacklistModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    referral_id = models.CharField(max_length=250)
