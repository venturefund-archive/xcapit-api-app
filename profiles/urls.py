from django.urls import path
from .views import ProfileAPIView

app_name = 'profiles'

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='retrieve-update-user-profile')
]
