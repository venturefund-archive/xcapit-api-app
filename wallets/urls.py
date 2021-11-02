from django.urls import path
from wallets.views import WalletsView, CreateNFTRequestView, NFTStatusView

app_name = 'wallets'

urlpatterns = [
    path('user/<user_id>/', WalletsView.as_view(), name='wallets'),
    path('request_nft/<user_id>', CreateNFTRequestView.as_view(), name='create-nft-request'),
    path('get_nft_status/<user_id>', NFTStatusView.as_view(), name='nft-status')
]
