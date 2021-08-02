from rest_framework import serializers
from .models import PaymentMethodModel


class PaymentMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethodModel
        fields = ['id', 'name', 'description', 'status']
