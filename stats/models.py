from django.db import models


class Logs(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    button_id = models.CharField(max_length=200, default='')
    component_id = models.CharField(max_length=200, default='')
    user_id = models.PositiveIntegerField(null=True, blank=True)
    ip = models.GenericIPAddressField(protocol='both', null=True, blank=True)
    agent = models.CharField(max_length=1000, null=True, blank=True, default='')
    event_id = models.CharField(max_length=200, default='')
    fired_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.user_id or "Not Logged User"} - {self.description}'

    class Meta:
        verbose_name = 'Logs'
        verbose_name_plural = 'Logs'

class LoginHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    ip = models.GenericIPAddressField(protocol='both', null=True, blank=True)
    logged = models.BooleanField()

    def __str__(self):
        return f'{self.created_at} - {self.email or "Not logged"}'

    class Meta:
        verbose_name = 'Login history'
        verbose_name_plural = 'Login history'
