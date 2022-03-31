from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.paginations import CustomPageNumberPagination
from wallets.serializers import WalletSerializer, NFTRequestSerializer, WalletSerializerWithoutUser
from django.shortcuts import get_object_or_404
from wallets.models import NFTRequest, Wallet
from users.models import User


class WalletsView(APIView):
    serializer_class = WalletSerializer

    @staticmethod
    def _add_user(item: dict, user_id: str):
        item['user'] = user_id
        return item

    def post(self, request, user_id):
        data = list(map(lambda item: self._add_user(item, user_id), request.data))
        serializer = self.serializer_class(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            response = Response({}, status=200)
        else:
            response = Response(serializer.errors, status=400)
        return response


class CreateNFTRequestView(APIView):
    serializer_class = NFTRequestSerializer

    def post(self, request, user_id):
        serializer = self.serializer_class(data={'user': user_id})
        if serializer.is_valid():
            serializer.save()
            response = Response({}, status=200)
        else:
            response = Response(serializer.errors, status=400)
        return response

    def put(self, request, user_id):
        nft_request = get_object_or_404(NFTRequest, user__id=user_id)
        nft_request.status = request.data.get('status')
        nft_request.save()
        return Response({}, status=200)


class NFTStatusView(APIView):
    serializer_class = NFTRequestSerializer

    def get(self, request, user_id):
        nft_request = get_object_or_404(NFTRequest, user__id=user_id)
        serializer = self.serializer_class(instance=nft_request)
        return Response(serializer.data, status=200)


class ClaimedNFTUsersView(APIView):

    def get(self, request):
        users = User.objects.filter(
            wallets__network='MATIC', nft__status='claimed'
        ).values('id', 'email', 'wallets__address')
        claimed_users = [{"id": user.get('id'),
                          "email": user.get('email'),
                          "address": user.get('wallets__address')}
                         for user in users]
        return Response(claimed_users, status=200)


class WalletAPIView(ModelViewSet):
    serializer_class = WalletSerializerWithoutUser
    pagination_class = CustomPageNumberPagination
    queryset = Wallet.objects.all()
