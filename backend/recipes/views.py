from rest_framework import viewsets, permissions, status
from recipes.models import Recipe, Ingredient, Tag, Favorite, Cart
from recipes.serializers import (
    PostRecipeSerializer, RecipeSerializer, IngredientSerializer,
    TagSerializer, ChooseRecipeSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.pagination import CustomizedPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomizedPagination

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        else:
            return PostRecipeSerializer
    
    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1':
            print(is_favorited)        
            return self.request.user.favorite.recipes.all()
        else:
            return Recipe.objects.all()
    


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
    serializer_class = ChooseRecipeSerializer

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Favorite.objects.get(user=request.user, recipe=recipe).delete()
        except Exception as error:
            raise ValidationError(error)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, serializer, *args, **kwargs):
        id = self.kwargs['id']
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Favorite.objects.create(user=self.request.user, recipe=recipe)
        except Exception as error:
            raise ValidationError(error)
        # return Response({
        #     "id": id,
        #     "name": serializer.data['name'],
        #     "image": serializer.data['image'],
        #     "cooking_time": serializer.data['cooking_time']
        # })
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    model = Recipe
    serializer_class = ChooseRecipeSerializer

    def create(self, serializer, *args, **kwargs):
        id = self.kwargs['id']
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Cart.objects.create(user=self.request.user, recipe=recipe)
        except Exception as error:
            raise ValidationError(error)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Cart.objects.get(user=request.user, recipe=recipe).delete()
        except Exception as error:
            raise ValidationError(error)
        
        return Response(status=status.HTTP_204_NO_CONTENT)