from users.models import User
from rest_framework import serializers
from wallets.models import Wallet, NFTRequest
from rest_framework.serializers import ModelSerializer


class WalletSerializer(serializers.Serializer):
    network = serializers.CharField(max_length=150)
    address = serializers.CharField(max_length=200)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        wallet, _ = Wallet.objects.update_or_create(
            user_id=validated_data['user'].id,
            network=validated_data.get('network'),
            defaults=validated_data
        )
        if validated_data.get('network') == 'ERC20':
            wallet.user.address = wallet.address
            wallet.user.save()

    def update(self, instance, validated_data):
        """"""


class NFTRequestSerializer(ModelSerializer):
    class Meta:
        model = NFTRequest
        fields = '__all__'


class WalletSerializerWithoutUser(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('address', 'network')
