from rest_framework.serializers import ModelSerializer
from users.models import User


class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'created_at', 'updated_at',
                  'password', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance
