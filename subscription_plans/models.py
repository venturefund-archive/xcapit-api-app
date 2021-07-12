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


class PlanModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    info = models.CharField(max_length=300)
    price = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=150, choices=PLAN_TYPE_CHOICES)
    state = models.CharField(max_length=150, choices=PLAN_STATE_CHOICES, blank=True)


class PlanSubscriptionModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.PROTECT)
