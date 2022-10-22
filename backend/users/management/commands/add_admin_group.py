from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'Adds admin group and sets every permission for admin models'

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='Admins')

        admin_perms_models = [
            ['view', 'change', 'add', 'delete'],
            {
                'recipe': Recipe,
                'ingredient': Ingredient,
                'recipeingredient': RecipeIngredient,
                'tag': Tag,
                'user': User
            },
            ]
        for perm in admin_perms_models[0]:
            for model_l, model in admin_perms_models[1].items():

                ct = ContentType.objects.get_for_model(model)

                if Permission.objects.filter(
                        codename=f'{perm}_{model_l}').exists():
                    Permission.objects.filter(
                        codename=f'{perm}_{model_l}').delete()

                new_perm, created = Permission.objects.get_or_create(
                    codename=f'{perm}_{model_l}', name=f'Can {perm} {model}',
                    content_type=ct)
                new_perm.save()
                admin_group.permissions.add(new_perm)
