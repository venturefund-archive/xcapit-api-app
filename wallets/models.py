from django.db import models
from users.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    created = models.DateTimeField(auto_now_add=True)
    network = models.CharField(max_length=150)
    address = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'network', 'address')
        ordering = ['user', 'created']
        verbose_name_plural = 'Wallets'
        verbose_name = 'Wallet'
