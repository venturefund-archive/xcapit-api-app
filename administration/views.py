from users.models import User
from .serializer import UserAdminSerializer
from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
from core.paginations import CustomCursorPaginationAPU
from administration.filters import UserFilterBackend
from rest_framework.filters import OrderingFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    pagination_class = CustomCursorPaginationAPU
    filter_backends = (OrderingFilter, UserFilterBackend)
    ordering_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# Las vistas siguientes deberian solo estar en apu
# class FundsListAPIView(APIView):

#     funds_service = FundsService()

#     def get(self, request):
#         return Response(self.funds_service.get_for_admin(request.GET),
#                         status.HTTP_200_OK)


# class FundStatusAdminAPIView(APIView):
#     runs_client = RunsClient()
#     estados_client = EstadosClient()
#     funds_service = FundsService()
#     subscriptions_service = SubscriptionsService()

#     def get(self, request, *args, **kwargs):
#         fund_name = kwargs['fund_name']
#         funds = self.runs_client.get_no_finalizado_by_nombre(fund_name)
#         funds = funds.json()
#         if len(funds) > 0:
#             fund = funds[0]
#             estados = self.estados_client.get_by_id_corrida(
#                 fund_name, fund['id_corrida']).json()
#             fund_status = self.funds_service.get_status(
#                 fund, estados) if len(estados) > 0 else None
#             response = Response(
#                 {'fund': fund, 'status': fund_status}, status.HTTP_200_OK)
#         else:
#             response = Response({}, status.HTTP_204_NO_CONTENT)

#         return response


# class FundBalanceAdminAPIView(APIView):
#     runs_client = RunsClient()
#     estados_client = EstadosClient()
#     funds_service = FundsService()

#     def get(self, request, *args, **kwargs):
#         fund_name = kwargs['fund_name']
#         last_run = self.runs_client.get_last_fund_run(fund_name).json()
#         if 'error' not in last_run:
#             last_run = last_run[0]
#             balance = self.estados_client.get_balance(
#                 fund_name, last_run['id_corrida']).json()
#             balance = balance if 'cant_btc' in balance else None
#             response = Response(
#                 {'fund': last_run, 'balance': balance}, status.HTTP_200_OK)
#         else:
#             response = Response(last_run, status.HTTP_400_BAD_REQUEST)

#         return response


# class SubscriptionsListAPIView(APIView):
#     subscriptions_service = SubscriptionsService()

#     def get(self, request, *args, **kwargs):
#         return Response(
#             self.subscriptions_service.get_subscriptions(
#                 kwargs.get('fund_name')),
#             status=status.HTTP_200_OK)


# class FundRunsAdminAPIView(APIView):
#     runs_service = RunsService()

#     def get(self, request, *args, **kwargs):
#         return Response(
#             self.runs_service.get_by_fund_name(
#                 fund_name=kwargs['fund_name'],
#                 state=kwargs['status']),
#             status.HTTP_200_OK)


# class StatusByRunIdAdminAPIView(APIView):
#     runs_client = RunsClient()
#     estados_client = EstadosClient()
#     funds_service = FundsService()

#     def get(self, request, *args, **kwargs):
#         run = self.runs_client.get_by_pk(kwargs['pk']).json()
#         response = Response({}, status.HTTP_204_NO_CONTENT)
#         if 'nombre_bot' in run:
#             estados = self.estados_client.get_fund_states(
#                 run['nombre_bot'],
#                 run['id_corrida']).json()
#             fund_status = self.funds_service.get_status(
#                 run, estados) if len(estados) > 0 else None
#             response = Response({'fund': run, 'status': fund_status},
#                                 status.HTTP_200_OK)

#         return response
