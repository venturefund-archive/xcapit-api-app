from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReferralSerializer
from .models import Referral
from rest_framework.views import APIView
from core.paginations import CustomCursorPaginationAPU
from .emails import ReferralEmail
from core.helpers import ResponseHelper
from users.models import User
add_error_code = ResponseHelper.add_error_code


class ReferralsViewSet(ModelViewSet):
    serializer_class = ReferralSerializer
    pagination_class = CustomCursorPaginationAPU
    queryset = Referral.objects.all()

    def create(self, request, user_id, *args, **kwargs):
        request.user = User.objects.get(pk=user_id)
        try:
            ReferralEmail.send(request.user, request.data['email'])
        except Exception:
            result = Response({'error': 'invalid data'},
                              status=status.HTTP_400_BAD_REQUEST)
            return add_error_code(result, 'referrals.create.emailDidNotSend')
        else:
            return super().create(request, *args, **kwargs)

    def retrieve(self, request, user_id):
        request.user = User.objects.get(pk=user_id)
        ordering = request.query_params.get('ordering', None)
        paginator = self.pagination_class(ordering=ordering.split(','))
        referrals = Referral.objects.filter(
            referral_id=request.user.referral_id)
        referrals_page = paginator.paginate_queryset(referrals, request)
        serializer = self.serializer_class(referrals_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    



# class UserReferralsAPIView(APIView):
#     serializer_class = ReferralSerializer
#     pagination_class = CustomCursorPaginationAPU

#     def get(self, request, user_id):
#         request.user = User.objects.get(pk=user_id)
#         ordering = request.query_params.get('ordering', None)
#         paginator = self.pagination_class(ordering=ordering.split(','))
#         referrals = Referral.objects.filter(
#             referral_id=request.user.referral_id)
#         referrals_page = paginator.paginate_queryset(referrals, request)
#         serializer = self.serializer_class(referrals_page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    
