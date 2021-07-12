# Generated by Django 3.0.2 on 2021-07-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0002_planmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planmodel',
            name='state',
            field=models.CharField(blank=True, choices=[('payment.licenses.annual', 'payment.licenses.annual'), ('payment.licenses.monthly', 'payment.licenses.monthly')], max_length=150),
        ),
        migrations.AlterField(
            model_name='planmodel',
            name='type',
            field=models.CharField(choices=[('free', 'free'), ('paid', 'paid'), ('premium', 'premium')], max_length=150),
        ),
    ]
