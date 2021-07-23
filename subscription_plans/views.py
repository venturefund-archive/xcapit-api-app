from datetime import datetime
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from subscription_plans.subscription_link import SubscriptionLink
from subscription_plans.models import PlanSubscriptionModel, PlanModel


class PaymentMethodsByPlanAPIView(APIView):

    def get(self, request, plan_id):
        return Response(data=[], status=status.HTTP_200_OK)


class FreePlanSubscriptionAPIView(APIView):

    def post(self, request):
        PlanSubscriptionModel(
            user=User.objects.get(pk=request.data.get('user_id')),
            plan=PlanModel.objects.get(type='free'),
            start_date=datetime.utcnow()
        ).save()
        return Response(data={}, status=status.HTTP_201_CREATED)


class PaidSubscriptionLinkAPIView(APIView):

    def post(self, request):
        subscription_link = SubscriptionLink.create(
            PlanModel.objects.get(id=request.data.get('plan_id')),
            User.objects.get(id=request.data.get('user_id'))
        )
        return Response({'link': subscription_link.value()}, status=status.HTTP_200_OK)
