from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from subscription_plans.models import PlanSubscriptionModel, PlanModel, PaymentMethodModel
from users.models import User


class PaymentMethodsByPlanAPIView(APIView):

    def get(self, request, plan_id):
        payment_methods = self.get_all_payment_methods() if plan_id != "1" else []
        return Response(data=payment_methods, status=status.HTTP_200_OK)

    @staticmethod
    def get_all_payment_methods():
        return list(PaymentMethodModel.objects.all().values('id', 'name', 'description'))


class FreePlanSubscriptionAPIView(APIView):

    def post(self, request):
        PlanSubscriptionModel(
            user=User.objects.get(pk=request.data.get('user_id')),
            plan=PlanModel.objects.get(type='free'),
            payment_method=PaymentMethodModel.objects.get(pk=1),
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=60),
            frequency=1,
            frequency_type='months',
            currency='ARS'
        ).save()
        return Response(data={}, status=status.HTTP_201_CREATED)
