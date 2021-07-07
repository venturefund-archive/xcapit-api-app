from django.db import models


class PlanSubscriptionModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    # plan = models.ForeignKey('plans.PlanModel', on_delete=models.deletion.PROTECT)
