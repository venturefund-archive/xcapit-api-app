from rest_framework import serializers
from .models import PaymentMethodModel, PlanModel


class PaymentMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethodModel
        fields = ['id', 'name', 'description', 'status']


class PlanModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanModel
        fields = ['id', 'name', 'info', 'price', 'type', 'frequency', 'frequency_type']
