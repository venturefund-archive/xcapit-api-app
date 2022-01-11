from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Referral
from .validators import AlreadyExistUserEmailValidator
from users.models import User


class ReferralSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Referral.objects.all(),
                message='referrals.create.referralAlreadyExist'
            ),
            AlreadyExistUserEmailValidator(
                queryset=User.objects.all(),
                message='referrals.create.referralAlreadyExistsAsUser'
            )
        ]
    )

    def parse_error(self):
        if len(self.errors['email']):
            return {'error_code': self.errors['email'][0]}
        return {}

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['referral_id'] = request.user.referral_id
        return super(ReferralSerializer, self).create(validated_data)

    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'accepted_at', 'referral_id')


