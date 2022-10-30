import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Adds all the ingredients to DB'

    def handle(self, *args, **kwargs):
        all_ingredients = []
        path = os.path.join(settings.BASE_DIR, 'data')
        f = open(os.path.join(path, 'ingredients.json'))
        data = json.load(f)
        for record in data:
            all_ingredients.append(Ingredient(
                name=record['name'],
                measurement_unit=record['measurement_unit']))
        Ingredient.objects.bulk_create(all_ingredients)
        f.close()
