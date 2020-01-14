from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = 'users'
    label = 'users'
    verbose_name = 'Users'

    def ready(self):
        import users.signals


default_app_config = 'users.UsersAppConfig'
