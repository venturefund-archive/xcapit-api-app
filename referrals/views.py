from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_app.settings import PWA_DOMAIN
from core.clients import NotificationsClient
from .serializers import ReferralSerializer
from .models import Referral
from core.paginations import CustomCursorPaginationAPU
from core.helpers import ResponseHelper
from users.models import User
from django.shortcuts import get_object_or_404
from .user_referrals import UserReferrals

add_error_code = ResponseHelper.add_error_code


class ReferralsViewSet(ModelViewSet):
    serializer_class = ReferralSerializer
    pagination_class = CustomCursorPaginationAPU
    queryset = Referral.objects.all()
    notifications_client = NotificationsClient()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.parse_error(), status=status.HTTP_400_BAD_REQUEST)

        request.user = User.objects.get(pk=kwargs.get('user_id'))
        email = request.data.get('email', None)
        data = self._create_data_for_notification(request.user, email)
        send_email_response = self.notifications_client.send_referral_email(data)

        if send_email_response.status_code != status.HTTP_200_OK:
            response = Response({'error': 'Email not sent'}, status=status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'referrals.create.emailDidNotSend')

        return super().create(request, *args, **kwargs)

    @staticmethod
    def _create_data_for_notification(user: User, referral_email: str):
        return {
            'referral_email': referral_email,
            'encode_email': force_str(urlsafe_base64_encode(force_bytes(referral_email))),
            'user_email': user.email,
            'referral_code': user.referral_id,
            'domain': PWA_DOMAIN
        }

    def retrieve(self, request, user_id):
        request.user = User.objects.get(pk=user_id)
        ordering = request.query_params.get('ordering', None)
        paginator = self.pagination_class(ordering=ordering.split(','))
        referrals = Referral.objects.filter(
            referral_id=request.user.referral_id)
        referrals_page = paginator.paginate_queryset(referrals, request)
        serializer = self.serializer_class(referrals_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReferralsCountView(APIView):

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not exist'}, status.HTTP_404_NOT_FOUND)
        referrals_count = Referral.objects.filter(
            referral_id=user.referral_id).count()

        return Response({'referrals_count': referrals_count}, status=status.HTTP_200_OK)


class UserReferralsCountView(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user_referrals_count = UserReferrals(user).to_dict()
        return Response(user_referrals_count, status.HTTP_200_OK)
