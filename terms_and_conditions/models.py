from django.db import models


class TermsAndConditions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    user_id = models.PositiveIntegerField()
