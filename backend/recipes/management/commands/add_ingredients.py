from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import json
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Adds all the ingredients to DB'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, '../data')
        f = open(os.path.join(path, 'ingredients.json'))
        data = json.load(f)
        for record in data:
            Ingredient.objects.create(
                name=record['name'],
                measurement_unit=record['measurement_unit'])
        f.close()
