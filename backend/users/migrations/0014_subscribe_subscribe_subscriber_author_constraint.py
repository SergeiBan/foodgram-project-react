# Generated by Django 4.1.2 on 2022-10-16 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_rename_authors_subscribe_author_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='subscribe_subscriber_author_constraint'),
        ),
    ]