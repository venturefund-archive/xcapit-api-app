from typing import Union
from rest_framework import serializers
import profiles.models
from .models import Profile
from surveys.user_investor_category import UserInvestorCategory


class PersonalDataSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.CharField(max_length=150, required=True, allow_blank=False, allow_null=False)
    cellphone = serializers.CharField(max_length=24, required=True, allow_blank=True, allow_null=False)

    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'cellphone')


class BillDataSerializer(serializers.ModelSerializer):
    condicion_iva = serializers.CharField(max_length=50, required=True, allow_blank=False, allow_null=False)
    tipo_factura = serializers.CharField(max_length=15, required=True, allow_blank=False, allow_null=False)
    cuit = serializers.CharField(max_length=15, required=True, allow_blank=False, allow_null=False)
    direccion = serializers.CharField(max_length=150, required=True, allow_blank=False, allow_null=False)
    pais = serializers.CharField(max_length=150, required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = Profile
        fields = ('condicion_iva', 'tipo_factura', 'cuit', 'direccion', 'pais')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.CharField(max_length=150, required=True, allow_blank=False, allow_null=False)
    cellphone = serializers.CharField(max_length=24, required=True, allow_blank=True, allow_null=False)
    condicion_iva = serializers.CharField(max_length=50, required=True, allow_blank=True, allow_null=True)
    tipo_factura = serializers.CharField(max_length=15, required=True, allow_blank=True, allow_null=True)
    cuit = serializers.CharField(max_length=15, required=True, allow_blank=True, allow_null=True)
    direccion = serializers.CharField(max_length=150, required=True, allow_blank=True, allow_null=True)
    pais = serializers.CharField(max_length=150, required=True, allow_blank=True, allow_null=True)
    lang = serializers.ChoiceField(choices=profiles.models.LANGUAGES, allow_null=True, allow_blank=True)
    notifications_enabled = serializers.BooleanField(required=False, allow_null=True)
    investor_score = serializers.IntegerField(min_value=0, max_value=18)
    investor_category = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'email', 'first_name', 'cellphone', 'condicion_iva',
            'tipo_factura', 'cuit', 'direccion', 'pais', 'lang',
            'notifications_enabled', 'investor_score', 'investor_category'
        )

    @staticmethod
    def get_investor_category(obj):
        return UserInvestorCategory(obj).value()


class ProfileSerializerFactory:

    @staticmethod
    def create(data_type: Union[str, None], *args, **kwargs):
        ser = None
        if data_type == 'personal_data':
            ser = PersonalDataSerializer(*args, **kwargs)
        elif data_type == 'bill_data':
            ser = BillDataSerializer(*args, **kwargs)
        elif data_type is None:
            ser = ProfileSerializer(*args, **kwargs)
        return ser
