from django.urls import path
from subscription_plans.views import PaymentMethodsByPlanAPIView, FreePlanSubscriptionAPIView, \
    PaidSubscriptionLinkAPIView

app_name = 'subscription_plans'

urlpatterns = [
    path('plans/<plan_id>/payment_methods', PaymentMethodsByPlanAPIView.as_view(), name='payment_methods_by_plan'),
    path('free_subscription/', FreePlanSubscriptionAPIView.as_view(), name='create_free_subscription'),
    path('paid_subscription_link/', PaidSubscriptionLinkAPIView.as_view(), name='paid_subscription_link'),
]
