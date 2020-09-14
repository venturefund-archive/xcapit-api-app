from django.contrib import admin
from .models import Logs, LoginHistory
# Register your models here.
admin.site.register(Logs)
admin.site.register(LoginHistory)
