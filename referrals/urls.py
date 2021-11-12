from django.urls import path
from .views import ReferralsViewSet, ReferralsCountView, UserReferralsCountView

app_name = 'referrals'

urlpatterns = [
    path('user/<user_id>', ReferralsViewSet.as_view({'post': 'create', 'get': 'retrieve'}), name="referrals"),
    path('count/user/<user_id>', ReferralsCountView.as_view(), name="count-referrals"),
    path('count_user_referrals/<user_id>', UserReferralsCountView.as_view(), name="get-user-referrals-count")
]
