from users.models import User
from rest_framework import serializers
from wallets.models import Wallet, NFTRequest
from rest_framework.serializers import ModelSerializer


class WalletSerializer(serializers.Serializer):
    network = serializers.CharField(max_length=150)
    address = serializers.CharField(max_length=200)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        network_wallet = validated_data.copy()
        del network_wallet['address']
        wallets = Wallet.objects.filter(**network_wallet)
        wallets.update(**validated_data) if len(wallets) > 0 else Wallet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """"""


class NFTRequestSerializer(ModelSerializer):
    class Meta:
        model = NFTRequest
        fields = '__all__'
