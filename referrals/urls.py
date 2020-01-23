from django.urls import path
from .views import ReferralsViewSet, UserReferralsAPIView

app_name = 'referrals'

urlpatterns = [
    path('user_referrals/user/<user_id>', UserReferralsAPIView.as_view(), name='user-referrals'),
    path('user/<user_id>', ReferralsViewSet.as_view({'post': 'create'}), name="referrals"),
]
