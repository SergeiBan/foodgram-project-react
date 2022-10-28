# Generated by Django 4.1.2 on 2022-10-12 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_remove_favorite_user_alter_favorite_recipes'),
        ('users', '0005_remove_user_subscriptions_user_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='recipes.favorite'),
        ),
    ]
