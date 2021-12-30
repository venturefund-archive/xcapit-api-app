from django.db import models

LANGUAGES = [
    ('es', 'es'),
    ('en', 'en')
]


class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=150, blank=True)

    last_name = models.CharField(max_length=150, blank=True)

    nro_dni = models.CharField(max_length=12, blank=True)

    cellphone = models.CharField(max_length=24, blank=True)

    condicion_iva = models.CharField(max_length=50, blank=True)

    tipo_factura = models.CharField(max_length=15, blank=True)

    cuit = models.CharField(max_length=15, blank=True)

    direccion = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    pais = models.CharField(max_length=150, blank=True)

    notifications_enabled = models.BooleanField(default=True)

    lang = models.CharField(max_length=30, choices=LANGUAGES, default='es')

    def __str__(self):
        return self.user.email
