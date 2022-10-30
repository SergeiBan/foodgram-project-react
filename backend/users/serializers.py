from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.mixins import IsSubscribed
from users.models import Subscribe

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(IsSubscribed, serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')


# Скопирован сюда для обхода проблем с циркулярным импортом
class ChooseRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
    read_only = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ()

    def validate(self, attrs):
        id = self.context['id']
        method = self.context['request'].method

        if not User.objects.filter(pk=id).exists():
            raise ValidationError('Такого автора нет.')

        user = self.context['request'].user
        author = User.objects.get(pk=id)
        if user == author:
            raise ValidationError('Нельзя быть подписанным на себя.')

        is_subscribed = Subscribe.objects.filter(
            subscriber=user, author=author).exists()
        if method == 'POST' and is_subscribed:
            raise ValidationError(
                'Вы уже подписаны на этого автора.')
        if method == 'DELETE' and not is_subscribed:
            raise ValidationError(
                'Вы не подписаны на этого автора.')

        return attrs


class SubscriptionSerializer(IsSubscribed, serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count')
        read_only = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ChooseRecipeSerializer(recipes, many=True).data
