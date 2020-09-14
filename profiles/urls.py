from django.urls import path
from .views import ProfileAPIView, ProfileValidAPIView

app_name = 'profiles'

urlpatterns = [
    path('user/<user_id>', ProfileAPIView.as_view(), name='retrieve-update-user-profile'),
    path('user/<user_id>/valid', ProfileValidAPIView.as_view(), name='valid'),
]
