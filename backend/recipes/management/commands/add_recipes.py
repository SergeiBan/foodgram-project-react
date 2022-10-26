from django.core.management.base import BaseCommand
from recipes.models import Ingredient, RecipeIngredient, Recipe, Tag
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile


User = get_user_model()


class Command(BaseCommand):
    help = 'Adds recipes to DB'

    def handle(self, *args, **kwargs):
        tag1 = Tag.objects.get_or_create(
            name='Завтрак', color='#FFEE00',
            slug='breakfast'
        )
        tag2 = Tag.objects.get_or_create(
            name='Обед', color='#EEFF00',
            slug='dinner'
        )
        tag3 = Tag.objects.get_or_create(
            name='Ужин', color='#FFDDEE',
            slug='supper'
        )

        ingredient1 = Ingredient.objects.get(pk=1)
        ingredient2 = Ingredient.objects.get(pk=2)
        ingredient3 = Ingredient.objects.get(pk=3)

        recipe_ingredient1 = RecipeIngredient.objects.get_or_create(
            ingredient=ingredient1,
            amount=3
        )
        recipe_ingredient2 = RecipeIngredient.objects.get_or_create(
            ingredient=ingredient2,
            amount=6
        )
        recipe_ingredient3 = RecipeIngredient.objects.get_or_create(
            ingredient=ingredient3,
            amount=9
        )

        data = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

        recipe1, created = Recipe.objects.get_or_create(
            name='Рецепт 1',
            author=User.objects.get(pk=1),
            image=data,
            text='Это первый рецепт',
            cooking_time=1
        )
        recipe1.tags.add(1, 2)
        recipe1.ingredients.add(1, 2)
