# Generated by Django 3.0.2 on 2022-01-03 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_notifications_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='investor_score',
            field=models.IntegerField(default=0),
        ),
    ]
