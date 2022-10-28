# Generated by Django 4.1.2 on 2022-10-16 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_subsciption_subscribe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribe',
            old_name='authors',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', to=settings.AUTH_USER_MODEL),
        ),
    ]
