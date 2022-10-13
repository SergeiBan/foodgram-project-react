from rest_framework import viewsets, permissions, status
from recipes.models import Recipe, Ingredient, Tag, Favorite
from recipes.serializers import (
    PostRecipeSerializer, RecipeSerializer, IngredientSerializer,
    TagSerializer, FavoriteSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        else:
            return PostRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    @action(detail=False, methods=['delete'])
    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        favorites = get_object_or_404(Favorite, user=request.user)
        if favorites.recipes.filter(pk=id).exists():
            favorites.recipes.remove(recipe)
            favorites.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Такого рецепта в избранном нет')

    def create(self, serializer, *args, **kwargs):
        id = self.kwargs['id']
        recipe = get_object_or_404(Recipe, pk=id)
        new_fav, _ = Favorite.objects.get_or_create(user=self.request.user)
        if new_fav.recipes.filter(pk=id):
            raise ValidationError('Рецепт уже добавлен в избранное')
        new_fav.recipes.add(recipe)
        new_fav.save()
        return Response({
            "id": id,
            "name": serializer.data['name'],
            "image": serializer.data['image'],
            "cooking_time": serializer.data['cooking_time']
        })
