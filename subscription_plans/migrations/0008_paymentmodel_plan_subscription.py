# Generated by Django 3.0.2 on 2021-07-15 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0007_paymentmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='plan_subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='subscription_plans.PlanSubscriptionModel'),
            preserve_default=False,
        ),
    ]
