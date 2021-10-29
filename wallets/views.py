from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.serializers import WalletSerializer


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
