from rest_framework import serializers

from users.models import User
from wallets.models import Wallet


class WalletSerializer(serializers.Serializer):
    network = serializers.CharField(max_length=150)
    address = serializers.CharField(max_length=200)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        Wallet.objects.get_or_create(**validated_data)

    def update(self, instance, validated_data):
        """"""
