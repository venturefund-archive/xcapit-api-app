from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from subscription_plans.models import PlanSubscriptionModel, PlanModel
from users.models import User


class PaymentMethodsByPlanAPIView(APIView):

    def get(self, request, plan_id):
        return Response(data=[], status=status.HTTP_200_OK)


class FreePlanSubscriptionAPIView(APIView):

    def post(self, request):
        PlanSubscriptionModel(
            user=User.objects.get(pk=request.data.get('user_id')),
            plan=PlanModel.objects.get(type='free')
        ).save()
        return Response(data={}, status=status.HTTP_201_CREATED)
