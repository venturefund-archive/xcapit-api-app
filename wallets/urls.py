from django.urls import path
from wallets.views import WalletsView, CreateNFTRequestView

app_name = 'wallets'

urlpatterns = [
    path('user/<user_id>/', WalletsView.as_view(), name='wallets'),
    path('request_nft/<user_id>', CreateNFTRequestView.as_view(), name='create-nft-request')
]
