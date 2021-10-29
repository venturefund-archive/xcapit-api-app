from django.db import models
from users.models import User

NFT_STATUS = [
    ('claimed', 'claimed'),
    ('delivered', 'delivered')
]


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='wallets')
    created = models.DateTimeField(auto_now_add=True)
    network = models.CharField(max_length=150)
    address = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'network', 'address')
        ordering = ['user', 'created']
        verbose_name_plural = 'Wallets'
        verbose_name = 'Wallet'


class NFTRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='nft', unique=True)
    status = models.CharField(max_length=30, choices=NFT_STATUS, default='claimed')
    claimed_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ['user', 'status']
        verbose_name_plural = 'NFTRequests'
        verbose_name = 'NFTRequest'
