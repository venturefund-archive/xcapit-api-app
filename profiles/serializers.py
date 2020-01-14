from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='user.email')

    first_name = serializers.CharField(max_length=150, allow_blank=True)

    last_name = serializers.CharField(max_length=150, allow_blank=True)

    nro_dni = serializers.CharField(max_length=12, allow_blank=True)

    cellphone = serializers.CharField(max_length=24, allow_blank=True)

    condicion_iva = serializers.CharField(max_length=50, allow_blank=True)

    tipo_factura = serializers.CharField(max_length=15, allow_blank=True)

    cuit = serializers.CharField(max_length=15, allow_blank=True)

    direccion = serializers.CharField(max_length=150, allow_blank=True)

    class Meta:
        model = Profile
        fields = (
            'email', 'first_name', 'last_name',
            'nro_dni', 'cellphone', 'condicion_iva',
            'tipo_factura', 'cuit', 'direccion',
        )
