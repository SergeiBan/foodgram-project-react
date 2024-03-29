# Generated by Django 4.1.2 on 2022-10-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_alter_recipeingredient_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
