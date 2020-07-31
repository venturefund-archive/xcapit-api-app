from django.contrib import admin
from terms_and_conditions.models import TermsAndConditions

# Register your models here.
class TermsAndConditionsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'accepted_at')

admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)