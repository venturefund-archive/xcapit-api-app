from rest_framework import serializers

from .models import TermsAndConditions


class TermsAndConditionsSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_id'] = request.user.id
        return super(TermsAndConditionsSerializer, self).create(validated_data)

    class Meta:
        model = TermsAndConditions
        fields = '__all__'
        read_only_fields = ('created_at', 'accepted_at', 'user_id')
