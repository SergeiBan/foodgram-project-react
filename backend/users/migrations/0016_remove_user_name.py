# Generated by Django 4.1.2 on 2022-10-19 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_user_subscriptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]