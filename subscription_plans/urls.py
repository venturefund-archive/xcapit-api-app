from django.urls import path
from subscription_plans.views import PaymentMethodsByPlanAPIView, FreePlanSubscriptionAPIView, \
    PaidSubscriptionLinkAPIView, MercadopagoWebhookAPIView, SubscriptionPlansAPIView

app_name = 'subscription_plans'

urlpatterns = [
    path('', SubscriptionPlansAPIView.as_view({'get': 'list'}), name='subscription_plans'),
    path('plans/payment_methods', PaymentMethodsByPlanAPIView.as_view({'get': 'list'}), name='payment_methods_by_plan'),
    path('free_subscription/', FreePlanSubscriptionAPIView.as_view(), name='create_free_subscription'),
    path('paid_subscription_link/', PaidSubscriptionLinkAPIView.as_view(), name='paid_subscription_link'),
    path('mercadopago_webhook/', MercadopagoWebhookAPIView.as_view(), name='mercadopago_webhook'),
]
