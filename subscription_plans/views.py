from datetime import datetime
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from subscription_plans.subscription import Subscription
from subscription_plans.mercadopago.mercadopago_webhook import MercadopagoWebhook
from subscription_plans.mercadopago.payment_created_event import PaymentCreatedEvent
from subscription_plans.models import PlanSubscriptionModel, PlanModel, PaymentMethodModel
from subscription_plans.serializers import PaymentMethodsSerializer


class PaymentMethodsByPlanAPIView(ReadOnlyModelViewSet):
    queryset = PaymentMethodModel.objects.all().exclude(status='inactive').order_by('status')
    serializer_class = PaymentMethodsSerializer
    paginator = None


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
        subscription = Subscription.create(self._create_plan_subscription(request))
        return Response({'link': subscription.created().link().value()}, status=status.HTTP_200_OK)

    @staticmethod
    def _create_plan_subscription(request):
        return PlanSubscriptionModel.objects.create(
            user=User.objects.get(id=request.data.get('user_id')),
            plan=PlanModel.objects.get(id=request.data.get('plan_id')),
            payment_method=PaymentMethodModel.objects.get(pk=request.data.get('payment_method_id')),
            start_date=datetime.utcnow(),
            currency='ARS',
            status='pending',
        )


class MercadopagoWebhookAPIView(APIView):
    def post(self, request):
        MercadopagoWebhook(request.data, {'payment.created': PaymentCreatedEvent.create}).dispatch_events()
        return Response({}, status=200)
