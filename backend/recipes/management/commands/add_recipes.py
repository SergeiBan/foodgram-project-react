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

        ingredients = list(Ingredient.objects.all()[:3])
        all_ingredients = [
            RecipeIngredient(ingredient=ingredients[0], amount=10),
            RecipeIngredient(ingredient=ingredients[1], amount=20),
            RecipeIngredient(ingredient=ingredients[2], amount=30)
        ]
        RecipeIngredient.objects.bulk_create(all_ingredients)

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
            step_bool = True
            first_val = 1 if step_bool else 2
            obj.tags.add(first_val, 3)
            obj.ingredients.add(first_val, 3)
            step_bool = not step_bool
