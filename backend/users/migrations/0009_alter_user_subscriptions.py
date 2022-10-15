# Generated by Django 4.1.2 on 2022-10-15 00:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_user_subscriptions_user_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subs', to=settings.AUTH_USER_MODEL),
        ),
    ]
