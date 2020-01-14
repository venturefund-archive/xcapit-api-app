from django.urls import path
from .views import UsersCountAPIView, \
    FundSummaryViewsAPIView, FundBalanceViewsAPIView, LogsViewSet, \
    LoginsCountAPIView, OpenCountAPIView, FundActionsCountAPIView, \
    PublicLogsViewSet

app_name = 'stats'

urlpatterns = [
    path('users/count', UsersCountAPIView.as_view(), name="count-users"),
    path('use/fund_summary_views', FundSummaryViewsAPIView.as_view(), name="count-fund-summary"),
    path('use/fund_balance_views', FundBalanceViewsAPIView.as_view(), name="count-fund-balance"),
    path('use/login_count', LoginsCountAPIView.as_view(), name="count-logins"),
    path('use/open_count', OpenCountAPIView.as_view(), name="count-opens"),
    path('use/fund_actions_count', FundActionsCountAPIView.as_view(), name="count-fund-actions"),
    path('logs', LogsViewSet.as_view({'get': 'list', 'post': 'create'}), name='logs'),
    path('public_logs', PublicLogsViewSet.as_view({'post': 'create'}), name='public-logs')
]
