from django.urls import path
from .views import ReferralsViewSet, UserReferralsAPIView

app_name = 'referrals'

urlpatterns = [
    path('user_referrals', UserReferralsAPIView.as_view(), name='user-referrals'),
    path('', ReferralsViewSet.as_view({'post': 'create'}), name="referrals"),
]
