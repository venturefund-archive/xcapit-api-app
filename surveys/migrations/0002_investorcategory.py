# Generated by Django 3.0.2 on 2022-01-03 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('range_from', models.IntegerField()),
                ('range_to', models.IntegerField()),
            ],
        ),
    ]
