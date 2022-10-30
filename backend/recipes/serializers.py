import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RetrieveRecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_id(self, obj):
        return obj.ingredient.id


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RetrieveRecipeIngredientSerializer(many=True)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Cart.objects.filter(user=user, recipe=obj).exists()


class PostRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'image', 'text', 'ingredients', 'tags',
            'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        new_recipe = Recipe.objects.create(
            author=self.context["request"].user, **validated_data)

        new_ris = []
        for ingredient in ingredients:
            ing = ingredient.get('ingredient')
            amt = ingredient.get('amount')
            new_ris.append(RecipeIngredient(ingredient=ing, amount=amt))

        objs = RecipeIngredient.objects.bulk_create(new_ris)

        new_recipe.tags.add(*tags)
        new_recipe.ingredients.add(*objs)

        new_recipe.save()
        return new_recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)

        instance.author = instance.author
        instance.image = validated_data['image']
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']

        new_ris = []
        for ingredient in ingredients:
            ing = ingredient.get('ingredient')
            amt = ingredient.get('amount')
            new_ris.append(RecipeIngredient(ingredient=ing, amount=amt))

        objs = RecipeIngredient.objects.bulk_create(new_ris)

        instance.ingredients.clear()
        instance.ingredients.add(*objs)

        instance.tags.clear()
        instance.tags.add(*tags)

        instance.save()
        return instance

    def validate_ingredients(self, value):
        all_ings = []
        for ingredient in value:
            ing_name = str(ingredient['ingredient'])
            all_ings.append(ing_name)

        non_unique = set([i for i in all_ings if all_ings.count(i) > 1])
        if non_unique:
            raise ValidationError(f'Ингредиент повторяется: {non_unique}')
        return value

    def validate_tags(self, value):
        non_unique = set([str(t) for t in value if value.count(t) > 1])

        if non_unique:
            raise ValidationError(f'Категория повторяется: {non_unique}')
        return value


class ChooseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
    read_only = ('id', 'name', 'image', 'cooking_time')


class RecipeAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ()

    def validate(self, attrs):
        id = self.context['id']
        method = self.context['request'].method
        destination = self.context['model']
        user = self.context['request'].user

        if not Recipe.objects.filter(pk=id).exists():
            raise ValidationError('Такого рецепта нет.')

        recipe = Recipe.objects.get(pk=id)
        is_added = destination.objects.filter(
            user=user, recipe=recipe).exists()
        if method == 'POST' and is_added:
            raise ValidationError(
                f'{destination.get_name()}: рецепт уже добавлен.')
        if method == 'DELETE' and not is_added:
            raise ValidationError(
                f'{destination.get_name()}: рецепта не содержится.')

        return attrs
