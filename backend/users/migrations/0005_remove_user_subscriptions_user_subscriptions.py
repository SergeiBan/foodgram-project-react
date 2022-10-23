# Generated by Django 4.1.2 on 2022-10-12 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='user',
            name='subscriptions',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to=settings.AUTH_USER_MODEL),
        ),
    ]
