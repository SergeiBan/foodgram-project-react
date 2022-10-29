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
        all_tags = [
            Tag(name='Завтрак', color='#FFEE00', slug='breakfast'),
            Tag(name='Обед', color='#EEFFFF', slug='dinner'),
            Tag(name='Ужин', color='#FFDDEE', slug='supper')
        ]
        Tag.objects.bulk_create(all_tags)

        # ingredients = list(Ingredient.objects.all()[:10])

        # all_recipe_ingredients = []
        # for i in range(len(list)):
        #     idx = random.randint(0, len(list) - 1)
        #     all_recipe_ingredients.append(
        #         RecipeIngredient(ingredient=ingredients[idx], amount = idx)

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

        authors = list(User.objects.all())

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
