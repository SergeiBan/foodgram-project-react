# Generated by Django 4.1.2 on 2022-10-14 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_remove_cart_recipes_cart_recipes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='recipes',
            new_name='recipe',
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user_recipe_constraint'),
        ),
    ]
