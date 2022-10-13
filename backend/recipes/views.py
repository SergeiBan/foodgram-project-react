from rest_framework import viewsets, permissions
from recipes.models import Recipe, Ingredient, Tag, Favorite
from recipes.serializers import (
    PostRecipeSerializer, RecipeSerializer, IngredientSerializer,
    TagSerializer, FavoriteSerializer)
from django.shortcuts import get_object_or_404


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

    # def perform_create(self, serializer):
    #     recipe = get_object_or_404(Recipe, pk=self.kwargs['id'])
    #     new_fav, _ = Favorite.objects.get_or_create(user=self.request.user)
    #     new_fav.recipes.add(recipe)
    #     new_fav.save()
    #     serializer.save()