from django.urls import path
from .views import ProfileAPIView

app_name = 'profiles'

urlpatterns = [
    path('user/<user_id>', ProfileAPIView.as_view(), name='retrieve-update-user-profile')
]
