from rest_framework import serializers
from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('network', 'address', 'user')

