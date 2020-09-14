from django.db import models


class TermsAndConditions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    user_id = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user_id} - {self.accepted}'

    class Meta:
        verbose_name = 'Terms and conditions'
        verbose_name_plural = 'Terms and conditions'
