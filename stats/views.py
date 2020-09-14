from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from rest_framework.viewsets import ModelViewSet
from .serializers import LogsSerializer
from .models import Logs
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from rest_framework.permissions import AllowAny
from .services import StatsService


class LogsViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LogsSerializer
    queryset = Logs.objects.all()
    pagination_class = None


class PublicLogsViewSet(ModelViewSet):
    serializer_class = LogsSerializer
    queryset = Logs.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)


class UsersCountAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        all_users = User.objects.all()
        if not year and not month:
            data = {
                'users': all_users.count(),
                'active': all_users.filter(is_active=True).count(),
                'inactive': all_users.filter(is_active=False).count()
            }
        elif year and not month:
            active_filter = Count('id', filter=Q(is_active=True))
            inactive_filter = Count('id', filter=Q(is_active=False))
            data = User.objects.filter(created_at__year=year) \
                .annotate(month=ExtractMonth('created_at')) \
                .values('month') \
                .annotate(users=Count('id')) \
                .annotate(active=active_filter) \
                .annotate(inactive=inactive_filter) \
                .values('month', 'users', 'active', 'inactive')
        else:
            month_users = all_users.filter(created_at__year=year,
                                           created_at__month=month)
            data = {
                'users': month_users.count(),
                'active': month_users.filter(is_active=True).count(),
                'inactive': month_users.filter(is_active=False).count()
            }

        return Response(data, status=status.HTTP_200_OK)


class FundSummaryViewsAPIView(APIView):
    permission_classes = (AllowAny,)
    stats_service = StatsService()

    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        count = self.stats_service.get_fund_summary_views(user_id)
        return Response(count, status=status.HTTP_200_OK)


class FundBalanceViewsAPIView(APIView):
    permission_classes = (AllowAny,)
    stats_service = StatsService()

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        count = self.stats_service.get_fund_balance_views(user_id)
        return Response(count, status=status.HTTP_200_OK)


class LoginsCountAPIView(APIView):
    permission_classes = (AllowAny,)
    stats_service = StatsService()

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        result = self.stats_service.get_login_count(user_id)
        return Response(result, status=status.HTTP_200_OK)


class OpenCountAPIView(APIView):
    permission_classes = (AllowAny,)
    stats_service = StatsService()

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        result = self.stats_service.get_open_count(user_id)
        return Response(result, status=status.HTTP_200_OK)


class FundActionsCountAPIView(APIView):
    permission_classes = (AllowAny,)
    stats_service = StatsService()

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        result = self.stats_service.get_fund_actions_count(user_id)
        return Response(result, status=status.HTTP_200_OK)
