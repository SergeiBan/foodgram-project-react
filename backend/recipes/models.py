from django.db import models
from django.contrib.auth import get_user_model
import io
from weasyprint import HTML


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        models.indexes = [
            models.Index(fields=['name'])
        ]


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


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
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return (
            f'{self.ingredient.name}, {self.ingredient.measurement_unit}: '
            f'{self.amount}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        verbose_name = 'В избранном'
        verbose_name_plural = 'В избранном'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_user_recipe_constraint')
        ]

    @classmethod
    def get_name(cls):
        return 'Избранное'


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name = 'В корзине'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='cart_user_recipe_constraint')
        ]

    @classmethod
    def get_shopping_list(cls, user):
        """
        Скачивает список ингредиентов для покупки.
        """
        buffer = io.BytesIO()
        total = {}

        cart_content = user.cart.prefetch_related(
            'recipe__ingredients').all()
        for cart_record in cart_content:
            ingredients = cart_record.recipe.ingredients.all()
            for ingredient in ingredients:
                if total.get(ingredient.ingredient):
                    total[ingredient.ingredient] += ingredient.amount
                else:
                    total[ingredient.ingredient] = ingredient.amount

        html_string = '<table><tr><th>Ингредиент</th><th>Количество</th></tr>'
        for key, val in total.items():
            html_string += f'<tr><td>{key}:</td><td>{val}</td></tr>'
        html_string += '</table>'
        HTML(string=html_string).write_pdf(buffer)

        buffer.seek(0)
        return buffer

    @classmethod
    def get_name(cls):
        return 'Корзина'
