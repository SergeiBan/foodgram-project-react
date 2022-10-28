from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class IsSubscribed():
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if (
            user.is_authenticated and user != obj
                and hasattr(user, 'authors')):
            return user.authors.filter(author=obj).exists()
        else:
            return False

    class Meta:
        abstract = True


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

        if not User.objects.filter(pk=id).exists():
            raise exceptions.ValidationError('Такого автора нет.')

        user = self.context['user']
        author = User.objects.get(pk=id)
        if user == author:
            raise exceptions.ValidationError('Нельзя подписаться на себя.')

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

    def validate(self, attrs):
        id = self.context['view'].kwargs.get('id')
        if User.objects.filter(pk=id).exists():
            author = User.objects.get(pk=id)
            user = self.context['request'].user
            if author == user:
                raise exceptions.ValidationError('Нельзя подписаться на себя.')
        else:
            raise exceptions.ValidationError('Такого автора нет.')

        return attrs
