from django.db import models


PLAN_TYPE_CHOICES = [
    ('free', 'free'),
    ('paid', 'paid'),
    ('premium', 'premium'),
]


PLAN_STATE_CHOICES = [
    ('payment.licenses.annual', 'payment.licenses.annual'),
    ('payment.licenses.monthly', 'payment.licenses.monthly'),
]


SUBSCRIPTION_STATUS_CHOICES = [
    ('pending', 'pending'),
    ('authorized', 'authorized'),
]


FREQUENCY_TYPE_CHOICES = [
    ('months', 'months'),
    ('years', 'years'),
]

PAYMENT_METHODS_STATUS_CHOICES = [
    ('active', 'active'),
    ('soon', 'soon'),
    ('inactive', 'inactive')
]


class PlanModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    info = models.CharField(max_length=300)
    price = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=150, choices=PLAN_TYPE_CHOICES)
    state = models.CharField(max_length=150, choices=PLAN_STATE_CHOICES, blank=True)
    frequency = models.PositiveIntegerField()
    frequency_type = models.CharField(max_length=100, choices=FREQUENCY_TYPE_CHOICES)


class PaymentMethodModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    payment_link = models.CharField(max_length=1000)
    provider_plan_id = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=PAYMENT_METHODS_STATUS_CHOICES)


class PlanSubscriptionModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethodModel, on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=15)
    status = models.CharField(max_length=150, choices=SUBSCRIPTION_STATUS_CHOICES)


class PaymentModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=30, decimal_places=15)
    currency = models.CharField(max_length=15)
    plan_subscription = models.ForeignKey(PlanSubscriptionModel, on_delete=models.PROTECT)
