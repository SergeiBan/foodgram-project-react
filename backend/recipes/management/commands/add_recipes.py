import base64
import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Adds recipes to DB'

    def handle(self, *args, **kwargs):
        all_tags = [
            Tag(name='Завтрак', color='#66OOCC', slug='breakfast'),
            Tag(name='Обед', color='#336600', slug='dinner'),
            Tag(name='Ужин', color='#99004C', slug='supper')
        ]
        Tag.objects.all().delete()
        Tag.objects.bulk_create(all_tags)

        ingredients = list(Ingredient.objects.all()[:3])
        all_ingredients = [
            RecipeIngredient(ingredient=ingredients[0], amount=10),
            RecipeIngredient(ingredient=ingredients[1], amount=20),
            RecipeIngredient(ingredient=ingredients[2], amount=30)
        ]
        RecipeIngredient.objects.all().delete()
        RecipeIngredient.objects.bulk_create(all_ingredients)

        path = os.path.join(settings.BASE_DIR, 'data')
        with open(os.path.join(path, 'testbase64pic.txt')) as f:
            file_data = f.read()

            format, imgstr = file_data.split(';base64,')
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
                    cooking_time=author_idx + 1))
            Recipe.objects.all().delete()
            recipes = Recipe.objects.bulk_create(recipes_data)

            for obj in recipes:
                # first_val = random.randint(1, 2)
                obj.tags.add(1, 3)
                obj.ingredients.add(1, 3)
