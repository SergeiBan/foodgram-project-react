from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.PositiveSmallIntegerField()
    units = models.CharField(max_length=16)


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=6, unique=True)
    slug = models.SlugField(max_length=16, unique=True)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=32)
    picture = models.ImageField()
    description = models.CharField(max_length=128)
    ingredient = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    duration = models.PositiveSmallIntegerField()
    in_cart = models.BooleanField(default=False)


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipe)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipe)