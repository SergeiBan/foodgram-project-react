from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    measurement_unit = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=16, unique=True)

    def __str__(self):
        return self.name


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
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.ingredient.name}, {self.ingredient.measurement_unit}: {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='favorite_user_recipe_constraint')
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='cart_user_recipe_constraint')
        ]