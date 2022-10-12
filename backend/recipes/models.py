from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    measurement_unit = models.CharField(max_length=16)


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=16, unique=True)


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(
        'RecipeIngredient', related_name='recipes')
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/', default=None, null=True)
    text = models.CharField(max_length=128)
    cooking_time = models.PositiveSmallIntegerField()


class RecipeIngredient(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)