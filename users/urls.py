from django.urls import path
from .views import RegistrationAPIView, EmailValidationTokenAPIView, \
    SendEmailValidationTokenAPIView, ObtainJWTView, \
    SendResetPasswordEmailAPIView, ResetPasswordAPIView, \
    ChangePasswordAPIView, IsSuperUserAPIView, GetUserAPIView

app_name = 'users'

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='user-registration'),
    path('email_validation', EmailValidationTokenAPIView.as_view(), name='email-validation'),
    path('login', ObtainJWTView.as_view(), name='user-login'),
    path('send_email_validation', SendEmailValidationTokenAPIView.as_view(), name='send-email-validation'),
    path('send_reset_password_email', SendResetPasswordEmailAPIView.as_view(), name='send-reset-password-email'),
    path('reset_password', ResetPasswordAPIView.as_view(), name="reset-password"),
    path('change_password/<pk>', ChangePasswordAPIView.as_view(), name="change-password"),
    path('is_superuser', IsSuperUserAPIView.as_view(), name='is-superuser'),
    path('<pk>', GetUserAPIView.as_view(), name='get-user'),
]
