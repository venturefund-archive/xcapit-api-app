# Generated by Django 3.0.2 on 2021-10-29 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallets', '0002_auto_20211028_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='NFTRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('claimed', 'claimed'), ('delivered', 'delivered')], default='claimed', max_length=30)),
                ('claimed_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='nft', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'NFTRequest',
                'verbose_name_plural': 'NFTRequests',
                'ordering': ['user', 'status'],
            },
        ),
    ]
