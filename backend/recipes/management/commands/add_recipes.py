import base64
import random

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Adds recipes to DB'

    def handle(self, *args, **kwargs):
        Tag.objects.get_or_create(
            name='Завтрак', color='#FFEE00',
            slug='breakfast'
        )
        Tag.objects.get_or_create(
            name='Обед', color='#EEFF00',
            slug='dinner'
        )
        Tag.objects.get_or_create(
            name='Ужин', color='#FFDDEE',
            slug='supper'
        )

        ingredient1 = Ingredient.objects.get(pk=1)
        ingredient2 = Ingredient.objects.get(pk=2)
        ingredient3 = Ingredient.objects.get(pk=3)

        RecipeIngredient.objects.get_or_create(
            ingredient=ingredient1,
            amount=3
        )
        RecipeIngredient.objects.get_or_create(
            ingredient=ingredient2,
            amount=6
        )
        RecipeIngredient.objects.get_or_create(
            ingredient=ingredient3,
            amount=9
        )

        data = (
            'data:image/gif;base64,R0lGODlhAQABAIAAAAAAA'
            'P///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

        authors = [
            User.objects.get(pk=1),
            User.objects.get(pk=2),
            User.objects.get(pk=3)
        ]

        recipes_data = []
        for n in range(20):
            author_idx = random.randint(0, len(authors) - 1)
            recipes_data.append(Recipe(
                name=f'Рецепт {n}',
                author=authors[author_idx],
                image=data,
                text=f'Это рецепт №{n}',
                cooking_time=author_idx))

        recipes = Recipe.objects.bulk_create(recipes_data)
        for obj in recipes:
            obj.tags.add(1, 2)
            obj.ingredients.add(1, 2)

        # recipe1, created = Recipe.objects.get_or_create(
        #     name='Рецепт 1',
        #     author=User.objects.get(pk=1),
        #     image=data,
        #     text='Это первый рецепт',
        #     cooking_time=1
        # )
        # recipe1.tags.add(1, 2)
        # recipe1.ingredients.add(1, 2)
