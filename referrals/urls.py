from django.urls import path
from .views import ReferralsViewSet

app_name = 'referrals'

urlpatterns = [
    path('user/<user_id>', ReferralsViewSet.as_view({'post': 'create', 'get': 'retrieve'}), name="referrals"),
]
