from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.serializers import WalletSerializer, NFTRequestSerializer
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


class NFTStatusView(APIView):
    serializer_class = NFTRequestSerializer

    def get(self, request, user_id):
        nft_request = get_object_or_404(NFTRequest, user__id=user_id)
        serializer = self.serializer_class(instance=nft_request)
        return Response(serializer.data, status=200)


class ClaimedNFTUsersView(APIView):

    def get(self, request):
        user_ids = NFTRequest.objects.select_related('user').filter(status="claimed").values_list('user_id', flat=True)
        wallets = Wallet.objects.select_related('user').filter(network='MATIC').values_list('user_id',
                                                                                            'user__email',
                                                                                            'address')

        claimed_users = [{"id": user_id, "email": email, "address": address}
                         for user_id, email, address in wallets
                         if user_id in user_ids]

        return Response(claimed_users, status=200)
