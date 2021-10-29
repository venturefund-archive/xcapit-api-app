from django.urls import path
from wallets.views import WalletsView

app_name = 'wallets'

urlpatterns = [
    path('user/<user_id>/', WalletsView.as_view(), name='wallets'),
]
