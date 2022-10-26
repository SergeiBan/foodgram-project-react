from rest_framework import serializers, exceptions
from recipes.models import (
    Recipe, Ingredient, Tag, RecipeIngredient, Favorite, Cart)
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
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

    def to_representation(self, value):
        return value.url


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
    image = Base64ImageField()

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

        for ingredient in ingredients:
            ing = ingredient.get('ingredient')
            amt = ingredient.get('amount')
            new_ri, _ = RecipeIngredient.objects.get_or_create(
                ingredient=ing, amount=amt)
            new_recipe.ingredients.add(new_ri)
        for tag in tags:
            new_recipe.tags.add(tag)

        new_recipe.save()
        return new_recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)

        try:
            instance.author = instance.author
            instance.image = validated_data['image']
            instance.name = validated_data['name']
            instance.text = validated_data['text']
            instance.cooking_time = validated_data['cooking_time']

            instance.ingredients.clear()
            for ingredient in ingredients:
                ing = ingredient.get('ingredient')
                amt = ingredient.get('amount')
                new_ri, _ = RecipeIngredient.objects.get_or_create(
                    ingredient=ing, amount=amt)
                instance.ingredients.add(new_ri)

            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)

            instance.save()
        except Exception as error:
            raise exceptions.ValidationError(error)
        return instance


class ChooseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
    read_only = ('id', 'name', 'image', 'cooking_time')
