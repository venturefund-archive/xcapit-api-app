from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='user.email')

    first_name = serializers.CharField(
        max_length=150,
        allow_blank=True,
        required=False
    )

    last_name = serializers.CharField(
        max_length=150,
        allow_blank=True,
        required=False
    )

    nro_dni = serializers.CharField(
        max_length=12,
        allow_blank=True,
        required=False
    )

    cellphone = serializers.CharField(
        max_length=24,
        allow_blank=True,
        required=False
    )

    condicion_iva = serializers.CharField(
        max_length=50,
        allow_blank=True,
        required=False
    )

    tipo_factura = serializers.CharField(
        max_length=15,
        allow_blank=True,
        required=False
    )

    cuit = serializers.CharField(
        max_length=15,
        allow_blank=True,
        required=False
    )

    direccion = serializers.CharField(
        max_length=150,
        allow_blank=True,
        required=False
    )

    pais = serializers.CharField(
        max_length=150,
        allow_blank=True,
        required=False
    )

    class Meta:
        model = Profile
        fields = (
            'email', 'first_name', 'last_name',
            'nro_dni', 'cellphone', 'condicion_iva',
            'tipo_factura', 'cuit', 'direccion', 'pais'
        )

    def validate(self, data):
        name_keys = {
            'first_name', 'last_name'
        }

        personal_data_keys = {
            'nro_dni', 'cellphone', 'cuit', 'direccion'
        }

        fiscal_data_keys = {
            'condicion_iva', 'tipo_factura',
            'cuit', 'pais'
        }

        all_keys = {
            'first_name', 'last_name',
            'nro_dni', 'cellphone', 'condicion_iva',
            'tipo_factura', 'cuit', 'direccion', 'pais'
        }

        if all(key in data.keys() for key in personal_data_keys):
            return data

        if all(key in data.keys() for key in fiscal_data_keys):
            return data

        if all(key in data.keys() for key in name_keys):
            return data

        if all(key in data.keys() for key in all_keys):
            return data

        raise serializers.ValidationError('This field must be an even number.')


class ProfileValidSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='user.email')

    first_name = serializers.CharField(max_length=150)

    last_name = serializers.CharField(max_length=150)

    nro_dni = serializers.CharField(max_length=12)

    cellphone = serializers.CharField(max_length=24)

    condicion_iva = serializers.CharField(max_length=50)

    tipo_factura = serializers.CharField(max_length=15)

    cuit = serializers.CharField(max_length=15)

    direccion = serializers.CharField(max_length=150)

    pais = serializers.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = (
            'email', 'first_name', 'last_name',
            'nro_dni', 'cellphone', 'condicion_iva',
            'tipo_factura', 'cuit', 'direccion', 'pais'
        )
