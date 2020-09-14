from django.contrib import admin
from users.models import User
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from users.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

admin.site.site_header = 'xcapit api-app'
admin.site.site_title = "xcapit api-app"
admin.site.index_title = "Admin"


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('last_login', )}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('last_login',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)