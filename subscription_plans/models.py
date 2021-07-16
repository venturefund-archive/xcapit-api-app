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


FREQUENCY_TYPE_CHOICES = [
    ('months', 'months'),
    ('years', 'years'),
]


class PlanModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    info = models.CharField(max_length=300)
    price = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=150, choices=PLAN_TYPE_CHOICES)
    state = models.CharField(max_length=150, choices=PLAN_STATE_CHOICES, blank=True)


class PaymentMethodModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)


class PlanSubscriptionModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethodModel, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    frequency = models.PositiveIntegerField()
    frequency_type = models.CharField(max_length=100, choices=FREQUENCY_TYPE_CHOICES)
    currency = models.CharField(max_length=15)


class PaymentModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=30, decimal_places=15)
    currency = models.CharField(max_length=15)
    plan_subscription = models.ForeignKey(PlanSubscriptionModel, on_delete=models.PROTECT)
