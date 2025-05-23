# Generated by Django 5.2 on 2025-05-15 05:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEarnings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit_per_hour', models.IntegerField(default=100)),
                ('last_claimed', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_collected', models.IntegerField(default=0)),
            ],
        ),
    ]
